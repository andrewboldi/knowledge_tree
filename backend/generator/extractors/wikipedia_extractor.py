"""Wikipedia content extractor for knowledge definitions."""

import re
import urllib.parse
import urllib.request
import json
from html import unescape

from .base import BaseExtractor, ExtractedConcept


class WikipediaExtractor(BaseExtractor):
    """Extract concept definitions from Wikipedia.

    Uses the Wikipedia API to fetch article summaries and extracts
    mathematical/scientific notation where available.
    """

    API_BASE = "https://en.wikipedia.org/api/rest_v1"
    WIKI_API = "https://en.wikipedia.org/w/api.php"

    def extract(self, term: str, domain: str, subfield: str) -> ExtractedConcept | None:
        """Extract concept from Wikipedia article."""
        # Fetch article summary
        summary = self._fetch_summary(term)
        if not summary:
            return None

        raw_definition = summary.get("extract", "")
        if not raw_definition:
            return None

        # Extract any LaTeX from the raw HTML content
        latex_fragments = []
        if html_content := summary.get("extract_html", ""):
            latex_fragments = self._extract_latex_from_html(html_content)

        # Build source URL
        title = summary.get("title", term)
        source_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"

        # Try to extract related concepts from links
        related_terms = self._fetch_related_terms(title)

        # Extract any mathematical notation patterns from the text
        notations = self._extract_notation_patterns(raw_definition)

        return ExtractedConcept(
            name=title,
            raw_definition=raw_definition,
            domain=domain,
            subfield=subfield,
            source_url=source_url,
            source_type="wikipedia",
            notations=notations,
            latex_fragments=latex_fragments,
            related_terms=related_terms[:10],  # Limit to 10 most relevant
            articles=[source_url],
        )

    def can_extract(self, term: str) -> bool:
        """Check if Wikipedia has an article for this term."""
        summary = self._fetch_summary(term)
        return summary is not None and "extract" in summary

    def _fetch_summary(self, term: str) -> dict | None:
        """Fetch article summary from Wikipedia REST API."""
        encoded_term = urllib.parse.quote(term.replace(" ", "_"))
        url = f"{self.API_BASE}/page/summary/{encoded_term}"

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "KnowledgeTree/1.0 (knowledge-tree-generator)"},
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    return json.loads(response.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
            pass
        return None

    def _fetch_related_terms(self, title: str) -> list[str]:
        """Fetch related terms via Wikipedia links API."""
        params = {
            "action": "query",
            "titles": title,
            "prop": "links",
            "pllimit": "50",
            "plnamespace": "0",
            "format": "json",
        }
        url = f"{self.WIKI_API}?{urllib.parse.urlencode(params)}"

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "KnowledgeTree/1.0 (knowledge-tree-generator)"},
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    pages = data.get("query", {}).get("pages", {})
                    for page in pages.values():
                        links = page.get("links", [])
                        return [link["title"] for link in links if "title" in link]
        except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
            pass
        return []

    def _extract_latex_from_html(self, html: str) -> list[str]:
        """Extract LaTeX notation from Wikipedia HTML."""
        fragments = []

        # Wikipedia uses various formats for math
        # <math> tags (rendered as images or MathML)
        math_pattern = re.compile(r"<math[^>]*>([^<]+)</math>", re.IGNORECASE)
        for match in math_pattern.finditer(html):
            latex = unescape(match.group(1)).strip()
            if latex:
                fragments.append(latex)

        # annotation-xml with LaTeX encoding
        annotation_pattern = re.compile(
            r'<annotation[^>]*encoding="application/x-tex"[^>]*>([^<]+)</annotation>',
            re.IGNORECASE,
        )
        for match in annotation_pattern.finditer(html):
            latex = unescape(match.group(1)).strip()
            if latex:
                fragments.append(latex)

        return fragments

    def _extract_notation_patterns(self, text: str) -> list[str]:
        """Extract mathematical notation patterns from plain text."""
        notations = []

        # Common notation patterns (simplified, LLM will formalize)
        # Variables like x, y, z, f(x)
        var_pattern = re.compile(r"\b[fghFGH]\s*\(\s*[xyztn]\s*\)")
        notations.extend(m.group() for m in var_pattern.finditer(text))

        # Greek letters written out
        greek = ["alpha", "beta", "gamma", "delta", "epsilon", "lambda", "sigma", "theta", "phi", "psi", "omega"]
        for letter in greek:
            if letter.lower() in text.lower():
                notations.append(letter)

        return list(set(notations))[:5]  # Dedupe and limit
