"""Web search content extractor for knowledge definitions."""

import os
import json
import urllib.parse
import urllib.request
from typing import Any

from .base import BaseExtractor, ExtractedConcept


class WebSearchExtractor(BaseExtractor):
    """Extract concept definitions from web search results.

    Uses search APIs to find authoritative sources for concepts,
    particularly useful for newer or more specialized topics not
    well-covered by Wikipedia.
    """

    # Trusted educational/scientific domains
    TRUSTED_DOMAINS = [
        "mathworld.wolfram.com",
        "encyclopediaofmath.org",
        "britannica.com",
        "stanford.edu",
        "mit.edu",
        "khanacademy.org",
        "nature.com",
        "sciencedirect.com",
        "arxiv.org",
    ]

    def __init__(self, search_api_key: str | None = None):
        """Initialize with optional search API key.

        Args:
            search_api_key: API key for search service. If not provided,
                            will attempt to read from SEARCH_API_KEY env var.
        """
        self.api_key = search_api_key or os.environ.get("SEARCH_API_KEY", "")

    def extract(self, term: str, domain: str, subfield: str) -> ExtractedConcept | None:
        """Extract concept from web search results."""
        search_results = self._search(term, domain)
        if not search_results:
            return None

        # Aggregate information from top results
        raw_definition = ""
        source_url = ""
        articles = []
        related_terms: list[str] = []

        for result in search_results[:5]:  # Top 5 results
            url = result.get("url", "")
            snippet = result.get("snippet", "")
            title = result.get("title", "")

            # Check if from trusted domain
            if any(trusted in url for trusted in self.TRUSTED_DOMAINS):
                if not raw_definition:
                    raw_definition = snippet
                    source_url = url
                articles.append(url)

            # Extract potential related terms from titles
            if title and title.lower() != term.lower():
                related_terms.append(title)

        if not raw_definition:
            # Fallback to first result if no trusted domains found
            if search_results:
                raw_definition = search_results[0].get("snippet", "")
                source_url = search_results[0].get("url", "")
                articles.append(source_url)

        if not raw_definition:
            return None

        return ExtractedConcept(
            name=term,
            raw_definition=raw_definition,
            domain=domain,
            subfield=subfield,
            source_url=source_url,
            source_type="web_search",
            related_terms=related_terms[:10],
            articles=articles,
        )

    def can_extract(self, term: str) -> bool:
        """Check if web search returns results for this term."""
        results = self._search(term, "")
        return bool(results)

    def _search(self, term: str, domain: str) -> list[dict[str, Any]]:
        """Perform web search for the term.

        This is a stub that should be implemented with an actual search API
        (e.g., Google Custom Search, Bing, SerpAPI).

        Returns:
            List of search results with 'url', 'title', 'snippet' keys.
        """
        if not self.api_key:
            # Return empty if no API key configured
            # In production, this would use a search API
            return self._fallback_search(term, domain)

        # Placeholder for actual search API integration
        # Example structure for Google Custom Search:
        # search_url = f"https://www.googleapis.com/customsearch/v1"
        # params = {
        #     "key": self.api_key,
        #     "cx": self.search_engine_id,
        #     "q": f"{term} {domain} definition"
        # }

        return self._fallback_search(term, domain)

    def _fallback_search(self, term: str, domain: str) -> list[dict[str, Any]]:
        """Fallback search using known URL patterns.

        Attempts to construct URLs for trusted sources directly.
        """
        results = []
        term_slug = term.lower().replace(" ", "_")
        term_hyphen = term.lower().replace(" ", "-")

        # MathWorld (for math terms)
        if domain.upper() == "MATH":
            mathworld_url = f"https://mathworld.wolfram.com/{term.replace(' ', '')}.html"
            results.append({
                "url": mathworld_url,
                "title": f"{term} -- from Wolfram MathWorld",
                "snippet": f"See the MathWorld entry for {term}.",
            })

        # Encyclopedia of Mathematics
        results.append({
            "url": f"https://encyclopediaofmath.org/wiki/{term_slug}",
            "title": f"{term} - Encyclopedia of Mathematics",
            "snippet": f"Encyclopedia of Mathematics article on {term}.",
        })

        # Stanford Encyclopedia (for logic/philosophy related)
        results.append({
            "url": f"https://plato.stanford.edu/entries/{term_hyphen}/",
            "title": f"{term} (Stanford Encyclopedia of Philosophy)",
            "snippet": f"Stanford Encyclopedia entry on {term}.",
        })

        return results

    def search_with_context(
        self, term: str, domain: str, subfield: str, prerequisites: list[str]
    ) -> list[dict[str, Any]]:
        """Search with additional context from prerequisites.

        Useful for disambiguating terms that have different meanings
        in different contexts.
        """
        context_terms = " ".join(prerequisites[:3])  # Use top 3 prerequisites
        query = f'"{term}" {domain} {subfield} {context_terms} definition'

        if self.api_key:
            # Would use actual search API here
            pass

        return self._search(term, domain)
