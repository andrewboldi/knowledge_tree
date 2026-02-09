"""LaTeX extractor - extracts and generates LaTeX notation."""


class LaTeXExtractor:
    """Extracts and generates LaTeX mathematical notation."""

    def extract_latex(self, text: str) -> list[str]:
        """Extract existing LaTeX expressions from text."""
        raise NotImplementedError("LaTeX extraction not yet implemented")

    def generate_latex(self, informal_math: str) -> str:
        """Convert informal mathematical notation to LaTeX."""
        raise NotImplementedError("LaTeX generation not yet implemented")
