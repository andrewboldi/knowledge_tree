"""Web search extractor - finds concept info via web search."""


class WebSearchExtractor:
    """Extracts concept definitions from web search results."""

    def extract(self, term: str, domain: str) -> dict | None:
        """
        Extract concept information via web search.

        Returns dict with name, definition, related terms, etc.
        Returns None if not found.
        """
        raise NotImplementedError("Web search extraction not yet implemented")
