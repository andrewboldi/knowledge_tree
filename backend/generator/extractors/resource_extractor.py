"""Resource extractor for books and academic papers."""

import os
import json
import re
import urllib.parse
import urllib.request
from typing import Any

from .base import BaseExtractor, ExtractedConcept


class ResourceExtractor(BaseExtractor):
    """Extract references to books and academic papers for concepts.

    Searches academic databases and book repositories to find
    authoritative resources for learning about concepts.
    """

    # Known textbook references by domain/subfield
    CANONICAL_TEXTBOOKS: dict[str, dict[str, list[str]]] = {
        "MATH": {
            "set_theory": [
                "Set Theory - Kenneth Kunen",
                "Naive Set Theory - Paul Halmos",
                "Set Theory: An Introduction to Independence Proofs - Kunen",
            ],
            "linear_algebra": [
                "Linear Algebra Done Right - Sheldon Axler",
                "Linear Algebra - Hoffman & Kunze",
                "Matrix Analysis - Horn & Johnson",
            ],
            "analysis": [
                "Principles of Mathematical Analysis - Walter Rudin",
                "Real and Complex Analysis - Walter Rudin",
                "Analysis I & II - Terence Tao",
            ],
            "topology": [
                "Topology - James Munkres",
                "General Topology - John Kelley",
                "Algebraic Topology - Allen Hatcher",
            ],
            "algebra": [
                "Abstract Algebra - Dummit & Foote",
                "Algebra - Serge Lang",
                "Basic Algebra I & II - Nathan Jacobson",
            ],
            "number_theory": [
                "An Introduction to the Theory of Numbers - Hardy & Wright",
                "A Classical Introduction to Modern Number Theory - Ireland & Rosen",
            ],
            "probability": [
                "Probability and Measure - Patrick Billingsley",
                "A First Course in Probability - Sheldon Ross",
            ],
        },
        "PHYSICS": {
            "mechanics": [
                "Classical Mechanics - Goldstein, Poole & Safko",
                "Mechanics - Landau & Lifshitz",
                "An Introduction to Mechanics - Kleppner & Kolenkow",
            ],
            "electromagnetism": [
                "Introduction to Electrodynamics - David Griffiths",
                "Classical Electrodynamics - John David Jackson",
                "The Feynman Lectures on Physics Vol. II",
            ],
            "quantum_mechanics": [
                "Principles of Quantum Mechanics - R. Shankar",
                "Introduction to Quantum Mechanics - David Griffiths",
                "Quantum Mechanics - Cohen-Tannoudji et al.",
            ],
            "thermodynamics": [
                "Thermal Physics - Charles Kittel",
                "Statistical Mechanics - R.K. Pathria",
            ],
        },
        "CHEMISTRY": {
            "general": [
                "Chemistry: The Central Science - Brown et al.",
                "Atkins' Physical Chemistry - Peter Atkins",
            ],
            "organic": [
                "Organic Chemistry - Clayden et al.",
                "March's Advanced Organic Chemistry - Smith & March",
            ],
            "physical": [
                "Physical Chemistry - Atkins & de Paula",
                "Molecular Quantum Mechanics - Atkins & Friedman",
            ],
        },
        "BIOLOGY": {
            "molecular": [
                "Molecular Biology of the Cell - Alberts et al.",
                "Molecular Biology of the Gene - Watson et al.",
            ],
            "genetics": [
                "Genetics: From Genes to Genomes - Hartwell et al.",
                "An Introduction to Genetic Analysis - Griffiths et al.",
            ],
            "biochemistry": [
                "Biochemistry - Stryer, Berg & Tymoczko",
                "Lehninger Principles of Biochemistry - Nelson & Cox",
            ],
        },
        "CS": {
            "algorithms": [
                "Introduction to Algorithms - Cormen et al. (CLRS)",
                "The Art of Computer Programming - Donald Knuth",
                "Algorithm Design - Kleinberg & Tardos",
            ],
            "complexity": [
                "Computational Complexity: A Modern Approach - Arora & Barak",
                "Introduction to the Theory of Computation - Michael Sipser",
            ],
            "programming_languages": [
                "Types and Programming Languages - Benjamin Pierce",
                "Structure and Interpretation of Computer Programs - Abelson & Sussman",
            ],
        },
    }

    ARXIV_API = "http://export.arxiv.org/api/query"
    CROSSREF_API = "https://api.crossref.org/works"

    def extract(self, term: str, domain: str, subfield: str) -> ExtractedConcept | None:
        """Extract resource references for a concept."""
        books = self._find_books(term, domain, subfield)
        papers = self._find_papers(term, domain)

        if not books and not papers:
            return None

        return ExtractedConcept(
            name=term,
            raw_definition="",  # Resource extractor doesn't provide definitions
            domain=domain,
            subfield=subfield,
            source_type="resource",
            books=books,
            papers=papers,
        )

    def can_extract(self, term: str) -> bool:
        """Resource extractor can always attempt to find resources."""
        return True

    def _find_books(self, term: str, domain: str, subfield: str) -> list[str]:
        """Find relevant textbooks for the concept."""
        books = []

        # Get canonical textbooks for the domain/subfield
        domain_books = self.CANONICAL_TEXTBOOKS.get(domain.upper(), {})
        subfield_books = domain_books.get(subfield, [])
        books.extend(subfield_books[:3])  # Top 3 for the subfield

        # Also check general domain books if subfield is not found
        if not subfield_books:
            # Try to find related subfields
            for sf, sf_books in domain_books.items():
                if sf in subfield or subfield in sf:
                    books.extend(sf_books[:2])
                    break

        return books

    def _find_papers(self, term: str, domain: str) -> list[str]:
        """Find relevant academic papers via arXiv API."""
        papers = []

        # Search arXiv for papers mentioning the term
        arxiv_results = self._search_arxiv(term, domain)
        for result in arxiv_results[:5]:
            arxiv_id = result.get("id", "")
            title = result.get("title", "")
            if arxiv_id:
                papers.append(f"arXiv:{arxiv_id} - {title}")

        # Could also add Crossref/DOI lookup here
        # crossref_results = self._search_crossref(term)

        return papers

    def _search_arxiv(self, term: str, domain: str) -> list[dict[str, Any]]:
        """Search arXiv for relevant papers."""
        # Map domains to arXiv categories
        arxiv_categories = {
            "MATH": "math",
            "PHYSICS": "physics",
            "CS": "cs",
            "BIOLOGY": "q-bio",
            "CHEMISTRY": "chem-ph",
        }

        category = arxiv_categories.get(domain.upper(), "")
        query = f'all:"{term}"'
        if category:
            query = f"cat:{category}.* AND {query}"

        params = {
            "search_query": query,
            "start": 0,
            "max_results": 5,
            "sortBy": "relevance",
        }
        url = f"{self.ARXIV_API}?{urllib.parse.urlencode(params)}"

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "KnowledgeTree/1.0"},
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status == 200:
                    content = response.read().decode("utf-8")
                    return self._parse_arxiv_response(content)
        except (urllib.error.HTTPError, urllib.error.URLError):
            pass

        return []

    def _parse_arxiv_response(self, xml_content: str) -> list[dict[str, Any]]:
        """Parse arXiv API XML response."""
        results = []

        # Simple regex parsing (could use xml.etree for production)
        entry_pattern = re.compile(r"<entry>(.*?)</entry>", re.DOTALL)
        id_pattern = re.compile(r"<id>http://arxiv.org/abs/([^<]+)</id>")
        title_pattern = re.compile(r"<title>([^<]+)</title>")

        for entry_match in entry_pattern.finditer(xml_content):
            entry = entry_match.group(1)

            arxiv_id = ""
            title = ""

            if id_match := id_pattern.search(entry):
                arxiv_id = id_match.group(1).strip()

            if title_match := title_pattern.search(entry):
                title = title_match.group(1).strip()
                # Clean up whitespace in title
                title = " ".join(title.split())

            if arxiv_id:
                results.append({"id": arxiv_id, "title": title})

        return results

    def enrich_concept(self, concept: ExtractedConcept) -> ExtractedConcept:
        """Add resource information to an existing extracted concept."""
        books = self._find_books(concept.name, concept.domain, concept.subfield)
        papers = self._find_papers(concept.name, concept.domain)

        concept.books.extend(b for b in books if b not in concept.books)
        concept.papers.extend(p for p in papers if p not in concept.papers)

        return concept
