"""Resource extractor - finds books, papers, and articles."""


class ResourceExtractor:
    """Extracts book, paper, and article references for concepts."""

    def extract_books(self, term: str, domain: str) -> list[str]:
        """Extract book references for a concept."""
        raise NotImplementedError("Book extraction not yet implemented")

    def extract_papers(self, term: str, domain: str) -> list[str]:
        """Extract paper references (arXiv, DOI) for a concept."""
        raise NotImplementedError("Paper extraction not yet implemented")

    def extract_articles(self, term: str, domain: str) -> list[str]:
        """Extract article URLs for a concept."""
        raise NotImplementedError("Article extraction not yet implemented")
