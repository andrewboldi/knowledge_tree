"""Forward pass engine for expanding knowledge from axioms.

The forward pass starts from foundational concepts (axioms) and expands outward
to discover related, more complex concepts. It's like building a tree from the
roots upward.
"""

import logging
import uuid
from dataclasses import dataclass
from typing import Protocol

from ..extractors import (
    ExtractedConcept,
    WikipediaExtractor,
    ResourceExtractor,
)
from .definition_formatter import DefinitionFormatter, RawConceptData, LLMClient


logger = logging.getLogger(__name__)


class ConceptStore(Protocol):
    """Protocol for concept storage operations."""

    def get_by_name(self, name: str) -> dict | None:
        """Get a concept by name."""
        ...

    def get_axioms(self, domain: str) -> list[dict]:
        """Get all axioms for a domain."""
        ...

    def get_by_complexity_range(
        self, domain: str, min_level: int, max_level: int
    ) -> list[dict]:
        """Get concepts within a complexity range."""
        ...

    def create(self, concept: dict) -> dict:
        """Create a new concept."""
        ...

    def add_requires(self, concept_id: str, prerequisite_id: str) -> None:
        """Add a REQUIRES relationship."""
        ...


@dataclass
class ForwardPassResult:
    """Result of a forward pass expansion."""

    concepts_added: int
    concepts_skipped: int
    errors: list[str]


class ForwardPassEngine:
    """Engine for forward pass expansion from axioms.

    The forward pass:
    1. Starts from existing axioms or low-complexity concepts
    2. Finds related terms mentioned in their definitions
    3. Extracts formal definitions for those terms
    4. Links new concepts back to their prerequisites
    """

    def __init__(
        self,
        store: ConceptStore,
        llm_client: LLMClient | None = None,
        wikipedia: WikipediaExtractor | None = None,
        resource_extractor: ResourceExtractor | None = None,
        formatter: DefinitionFormatter | None = None,
    ):
        self.store = store
        self.wikipedia = wikipedia or WikipediaExtractor()
        self.resource_extractor = resource_extractor or ResourceExtractor()
        self.formatter = formatter or DefinitionFormatter(llm_client)

    def execute(
        self, domains: list[str], target_count: int, max_complexity: int = 3
    ) -> ForwardPassResult:
        """Execute a forward pass to expand knowledge.

        Args:
            domains: Domains to expand (e.g., ["MATH", "PHYSICS"])
            target_count: Target number of new concepts to add
            max_complexity: Maximum complexity level to explore from

        Returns:
            ForwardPassResult with statistics
        """
        added = 0
        skipped = 0
        errors: list[str] = []

        for domain in domains:
            if added >= target_count:
                break

            # Get seed concepts to expand from (axioms and low-complexity)
            seeds = self._get_seed_concepts(domain, max_complexity)

            for seed in seeds:
                if added >= target_count:
                    break

                # Extract related terms from the seed concept
                related_terms = self._extract_related_terms(seed)

                for term in related_terms:
                    if added >= target_count:
                        break

                    # Check if concept already exists
                    if self.store.get_by_name(term):
                        skipped += 1
                        continue

                    try:
                        concept = self._extract_and_create_concept(
                            term=term,
                            domain=domain,
                            subfield=seed.get("subfield", "general"),
                            prerequisite_id=seed.get("id"),
                            base_complexity=seed.get("complexity_level", 0),
                        )
                        if concept:
                            added += 1
                            logger.info(f"Forward pass: Added '{term}' (from {seed.get('name')})")
                        else:
                            skipped += 1
                    except Exception as e:
                        errors.append(f"Failed to create '{term}': {e}")
                        logger.warning(f"Forward pass error for '{term}': {e}")

        return ForwardPassResult(
            concepts_added=added,
            concepts_skipped=skipped,
            errors=errors,
        )

    def _get_seed_concepts(self, domain: str, max_complexity: int) -> list[dict]:
        """Get concepts to expand from.

        Prioritizes axioms, then low-complexity concepts.
        """
        seeds = []

        # First, get axioms
        axioms = self.store.get_axioms(domain)
        seeds.extend(axioms)

        # Then get low-complexity concepts (up to max_complexity)
        if len(seeds) < 20:  # Limit seed count
            low_complexity = self.store.get_by_complexity_range(
                domain, 1, max_complexity
            )
            # Shuffle to get variety
            import random
            random.shuffle(low_complexity)
            seeds.extend(low_complexity[: 20 - len(seeds)])

        return seeds

    def _extract_related_terms(self, concept: dict) -> list[str]:
        """Extract terms mentioned in a concept's definition that could be expanded.

        Looks for:
        - Explicitly listed related_concepts
        - Bolded terms in the definition
        - Mathematical terms referenced
        """
        terms = []

        # First, use explicitly listed related concepts
        if related := concept.get("related_concepts"):
            terms.extend(related)

        # Extract bolded terms from definition (Markdown **term**)
        definition = concept.get("definition_md", "")
        import re
        bold_pattern = re.compile(r"\*\*([^*]+)\*\*")
        for match in bold_pattern.finditer(definition):
            term = match.group(1).strip()
            # Filter out common non-concept phrases
            if self._is_likely_concept(term):
                terms.append(term)

        # Look for "see also" or "related:" patterns
        see_also_pattern = re.compile(r"(?:see also|related|cf\.?)[:\s]+([^.\n]+)", re.I)
        for match in see_also_pattern.finditer(definition):
            for term in match.group(1).split(","):
                term = term.strip()
                if term and self._is_likely_concept(term):
                    terms.append(term)

        # Deduplicate while preserving order
        seen = set()
        unique_terms = []
        for term in terms:
            if term.lower() not in seen and term != concept.get("name"):
                seen.add(term.lower())
                unique_terms.append(term)

        return unique_terms[:10]  # Limit to 10 terms

    def _is_likely_concept(self, term: str) -> bool:
        """Check if a term is likely to be a mathematical/scientific concept."""
        # Filter out common words and short terms
        if len(term) < 3:
            return False

        # Filter out common phrases that aren't concepts
        non_concepts = {
            "example", "examples", "note", "notes", "proof", "see",
            "that is", "i.e.", "e.g.", "definition", "theorem", "lemma",
            "informal", "formal", "property", "properties", "consequence",
        }
        if term.lower() in non_concepts:
            return False

        # Concepts usually start with capital letter or are known patterns
        if term[0].isupper():
            return True

        # Greek letters are often concepts
        greek = ["alpha", "beta", "gamma", "delta", "omega", "sigma", "pi"]
        if term.lower() in greek:
            return True

        return False

    def _extract_and_create_concept(
        self,
        term: str,
        domain: str,
        subfield: str,
        prerequisite_id: str | None,
        base_complexity: int,
    ) -> dict | None:
        """Extract concept data and create it in the store.

        Args:
            term: The concept name to create
            domain: The domain (MATH, PHYSICS, etc.)
            subfield: The subfield
            prerequisite_id: ID of the concept this was derived from
            base_complexity: Complexity of the prerequisite

        Returns:
            Created concept dict, or None if extraction failed
        """
        # Try Wikipedia first
        extracted: ExtractedConcept | None = None
        if self.wikipedia.can_extract(term):
            extracted = self.wikipedia.extract(term, domain, subfield)

        if not extracted:
            # No Wikipedia content, create minimal concept from LLM
            extracted = ExtractedConcept(
                name=term,
                raw_definition="",  # LLM will generate
                domain=domain,
                subfield=subfield,
            )

        # Enrich with resources (books, papers)
        extracted = self.resource_extractor.enrich_concept(extracted)

        # Format definition with LaTeX
        raw_data = RawConceptData(
            name=extracted.name,
            domain=extracted.domain,
            subfield=extracted.subfield,
            definition=extracted.raw_definition,
            notations=extracted.notations,
            examples=extracted.examples,
        )
        formatted_definition = self.formatter.format_definition(raw_data)

        # Calculate complexity (one level above prerequisite)
        complexity = base_complexity + 1

        # Generate concept ID
        concept_id = self._generate_id(domain, subfield, term)

        # Create the concept
        concept = {
            "id": concept_id,
            "name": term,
            "definition_md": formatted_definition,
            "domain": domain,
            "subfield": subfield,
            "complexity_level": complexity,
            "books": extracted.books,
            "papers": extracted.papers,
            "articles": extracted.articles,
            "related_concepts": extracted.related_terms,
            "llm_summary": "",
            "is_axiom": False,
            "is_verified": False,
        }

        created = self.store.create(concept)

        # Link to prerequisite
        if prerequisite_id:
            self.store.add_requires(concept_id, prerequisite_id)

        # Link to any mentioned prerequisites
        for prereq_name in extracted.prerequisites:
            prereq = self.store.get_by_name(prereq_name)
            if prereq:
                self.store.add_requires(concept_id, prereq["id"])

        return created

    def _generate_id(self, domain: str, subfield: str, name: str) -> str:
        """Generate a unique concept ID."""
        name_slug = name.lower().replace(" ", "-")[:20]
        short_uuid = uuid.uuid4().hex[:8]
        return f"{domain.lower()}-{subfield}-{name_slug}-{short_uuid}"
