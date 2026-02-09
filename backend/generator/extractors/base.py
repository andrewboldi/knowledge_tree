"""Base extractor class and common types."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ExtractedConcept:
    """Raw concept data extracted from a source.

    This is the intermediate format before being processed by the
    DefinitionFormatter into the final Concept with Markdown + LaTeX.
    """

    name: str
    raw_definition: str  # May lack LaTeX, will be formalized
    domain: str  # MATH, PHYSICS, CHEMISTRY, BIOLOGY, CS
    subfield: str

    # Source information
    source_url: str = ""
    source_type: str = ""  # wikipedia, web, book, paper

    # Optional extracted data
    notations: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    related_terms: list[str] = field(default_factory=list)

    # Resources
    books: list[str] = field(default_factory=list)
    papers: list[str] = field(default_factory=list)
    articles: list[str] = field(default_factory=list)

    # Extracted LaTeX (if already present in source)
    latex_fragments: list[str] = field(default_factory=list)


class BaseExtractor(ABC):
    """Base class for all content extractors.

    Each extractor takes a concept name (and optional context) and
    returns structured data suitable for the DefinitionFormatter.
    """

    @abstractmethod
    def extract(self, term: str, domain: str, subfield: str) -> ExtractedConcept | None:
        """Extract concept information for a given term.

        Args:
            term: The concept name to extract (e.g., "Vector Space")
            domain: The domain (MATH, PHYSICS, etc.)
            subfield: The subfield (linear_algebra, mechanics, etc.)

        Returns:
            ExtractedConcept with raw data, or None if extraction fails.
        """
        pass

    @abstractmethod
    def can_extract(self, term: str) -> bool:
        """Check if this extractor can handle the given term.

        Returns:
            True if the extractor has data for this term.
        """
        pass
