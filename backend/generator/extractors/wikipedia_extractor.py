"""Wikipedia extractor - extracts concept information from Wikipedia."""


class WikipediaExtractor:
    """Extracts concept definitions and related info from Wikipedia."""

    def extract(self, term: str, domain: str) -> dict | None:
        """
        Extract concept information from Wikipedia.

        Returns dict with name, definition, related terms, etc.
        Returns None if not found.
        """
        raise NotImplementedError("Wikipedia extraction not yet implemented")
