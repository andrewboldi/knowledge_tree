"""Backward pass engine for tracing prerequisites from complex concepts.

The backward pass starts from complex, high-level concepts and works backward
to discover the fundamental concepts they depend on. It's like reverse-engineering
a tree from the leaves down to the roots.
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

    def get_complex_concepts(self, domain: str, min_level: int) -> list[dict]:
        """Get concepts at or above a complexity level."""
        ...

    def get_incomplete_concepts(self, domain: str) -> list[dict]:
        """Get concepts that have unresolved prerequisites."""
        ...

    def create(self, concept: dict) -> dict:
        """Create a new concept."""
        ...

    def add_requires(self, concept_id: str, prerequisite_id: str) -> None:
        """Add a REQUIRES relationship."""
        ...

    def update_prerequisites(self, concept_id: str, prereq_names: list[str]) -> None:
        """Update concept's list of prerequisite names."""
        ...


@dataclass
class BackwardPassResult:
    """Result of a backward pass expansion."""

    concepts_added: int
    concepts_skipped: int
    prerequisites_linked: int
    errors: list[str]


class BackwardPassEngine:
    """Engine for backward pass - tracing prerequisites from complex terms.

    The backward pass:
    1. Picks complex concepts with missing prerequisites
    2. Analyzes what simpler concepts they depend on
    3. Creates those prerequisite concepts if they don't exist
    4. Links the dependency chain
    """

    # Common prerequisite terms that should exist for various domains
    DOMAIN_FUNDAMENTALS: dict[str, list[str]] = {
        "MATH": [
            "Set", "Function", "Relation", "Ordered Pair", "Subset",
            "Cardinality", "Bijection", "Injection", "Surjection",
            "Equivalence Relation", "Partial Order", "Total Order",
        ],
        "PHYSICS": [
            "Force", "Energy", "Momentum", "Mass", "Velocity", "Acceleration",
            "Work", "Power", "Vector", "Scalar", "Field",
        ],
        "CHEMISTRY": [
            "Atom", "Molecule", "Element", "Compound", "Chemical Bond",
            "Electron", "Proton", "Neutron", "Ion", "Covalent Bond",
        ],
        "BIOLOGY": [
            "Cell", "DNA", "RNA", "Protein", "Gene", "Chromosome",
            "Nucleus", "Mitochondria", "Enzyme", "Metabolism",
        ],
        "CS": [
            "Algorithm", "Data Structure", "Complexity", "Function",
            "Variable", "Type", "Graph", "Tree", "Set", "Recursion",
        ],
    }

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
        self, domains: list[str], target_count: int, min_complexity: int = 2
    ) -> BackwardPassResult:
        """Execute a backward pass to discover prerequisites.

        Args:
            domains: Domains to analyze (e.g., ["MATH", "PHYSICS"])
            target_count: Target number of new concepts to add
            min_complexity: Minimum complexity level to trace back from

        Returns:
            BackwardPassResult with statistics
        """
        added = 0
        skipped = 0
        linked = 0
        errors: list[str] = []

        for domain in domains:
            if added >= target_count:
                break

            # Get complex concepts to trace back from
            complex_concepts = self._get_complex_concepts(domain, min_complexity)

            for concept in complex_concepts:
                if added >= target_count:
                    break

                # Find prerequisite terms
                prereq_terms = self._find_prerequisites(concept, domain)

                for term in prereq_terms:
                    if added >= target_count:
                        break

                    # Check if prerequisite exists
                    existing = self.store.get_by_name(term)
                    if existing:
                        # Just link it
                        self.store.add_requires(concept["id"], existing["id"])
                        linked += 1
                        continue

                    # Create the prerequisite
                    try:
                        prereq_concept = self._create_prerequisite(
                            term=term,
                            domain=domain,
                            subfield=concept.get("subfield", "general"),
                            dependent_concept=concept,
                        )
                        if prereq_concept:
                            # Link to the concept that needs it
                            self.store.add_requires(concept["id"], prereq_concept["id"])
                            added += 1
                            linked += 1
                            logger.info(
                                f"Backward pass: Added prerequisite '{term}' "
                                f"(needed by {concept.get('name')})"
                            )
                        else:
                            skipped += 1
                    except Exception as e:
                        errors.append(f"Failed to create prerequisite '{term}': {e}")
                        logger.warning(f"Backward pass error for '{term}': {e}")

        return BackwardPassResult(
            concepts_added=added,
            concepts_skipped=skipped,
            prerequisites_linked=linked,
            errors=errors,
        )

    def _get_complex_concepts(self, domain: str, min_level: int) -> list[dict]:
        """Get complex concepts that may have unlinked prerequisites."""
        # First try to get concepts with missing prereqs
        incomplete = self.store.get_incomplete_concepts(domain)
        if incomplete:
            return incomplete[:20]

        # Otherwise, get high-complexity concepts
        complex_concepts = self.store.get_complex_concepts(domain, min_level)

        # Shuffle for variety
        import random
        random.shuffle(complex_concepts)

        return complex_concepts[:20]

    def _find_prerequisites(self, concept: dict, domain: str) -> list[str]:
        """Analyze a concept to find what prerequisites it needs.

        Looks for:
        - Referenced terms in the definition
        - Domain fundamental terms that should be understood
        - Terms in the "requires" or prerequisite mentions
        """
        prereqs = []
        definition = concept.get("definition_md", "")

        # Check for explicitly mentioned prerequisites
        import re

        # Pattern: "requires understanding of X" or "assumes knowledge of X"
        requires_pattern = re.compile(
            r"(?:requires?|assumes?|needs?|depends? on)[:\s]+([^.\n]+)",
            re.I,
        )
        for match in requires_pattern.finditer(definition):
            for term in match.group(1).split(","):
                term = term.strip()
                if term and len(term) > 2:
                    prereqs.append(term)

        # Look for "see" references
        see_pattern = re.compile(r"(?:see|cf\.?)\s+\*\*([^*]+)\*\*", re.I)
        for match in see_pattern.finditer(definition):
            prereqs.append(match.group(1).strip())

        # Check domain fundamentals - concepts that should exist
        fundamentals = self.DOMAIN_FUNDAMENTALS.get(domain.upper(), [])
        for fundamental in fundamentals:
            # Check if the fundamental is referenced in the definition
            if fundamental.lower() in definition.lower():
                prereqs.append(fundamental)

        # Extract parenthetical definitions that reference other concepts
        # E.g., "...a vector space (see Vector Space)..."
        paren_pattern = re.compile(r"\((?:see|from|as defined in)\s+([^)]+)\)", re.I)
        for match in paren_pattern.finditer(definition):
            prereqs.append(match.group(1).strip())

        # Use LLM to identify prerequisites if we found few
        if len(prereqs) < 3:
            llm_prereqs = self._identify_prerequisites_with_llm(concept, domain)
            prereqs.extend(llm_prereqs)

        # Deduplicate and filter
        seen = set()
        unique_prereqs = []
        concept_name = concept.get("name", "").lower()
        for term in prereqs:
            term_lower = term.lower()
            if (
                term_lower not in seen
                and term_lower != concept_name
                and len(term) > 2
            ):
                seen.add(term_lower)
                unique_prereqs.append(term)

        return unique_prereqs[:8]  # Limit to 8 prerequisites

    def _identify_prerequisites_with_llm(
        self, concept: dict, domain: str
    ) -> list[str]:
        """Use LLM to identify what concepts are prerequisites."""
        name = concept.get("name", "")
        definition = concept.get("definition_md", "")

        prompt = f"""Given this {domain} concept and its definition, identify the 3-5 most important
prerequisite concepts that a learner must understand BEFORE they can understand this concept.

Concept: {name}
Definition:
{definition[:500]}

Return ONLY a comma-separated list of prerequisite concept names. Be specific and use standard
mathematical/scientific terminology. Example output:
Set, Function, Ordered Pair, Relation

Prerequisites:"""

        try:
            # Use the formatter's LLM client
            result = self.formatter._llm.complete(prompt)
            # Parse comma-separated list
            prereqs = [p.strip() for p in result.split(",") if p.strip()]
            return prereqs[:5]
        except Exception as e:
            logger.warning(f"LLM prerequisite identification failed: {e}")
            return []

    def _create_prerequisite(
        self,
        term: str,
        domain: str,
        subfield: str,
        dependent_concept: dict,
    ) -> dict | None:
        """Create a prerequisite concept.

        Prerequisites are created with complexity one level below
        the concept that depends on them.
        """
        # Extract from Wikipedia
        extracted: ExtractedConcept | None = None
        if self.wikipedia.can_extract(term):
            extracted = self.wikipedia.extract(term, domain, subfield)

        if not extracted:
            # Create minimal concept from LLM
            extracted = ExtractedConcept(
                name=term,
                raw_definition="",  # LLM will generate
                domain=domain,
                subfield=subfield,
            )

        # Enrich with resources
        extracted = self.resource_extractor.enrich_concept(extracted)

        # Format definition
        raw_data = RawConceptData(
            name=extracted.name,
            domain=extracted.domain,
            subfield=extracted.subfield,
            definition=extracted.raw_definition,
            notations=extracted.notations,
            examples=extracted.examples,
        )
        formatted_definition = self.formatter.format_definition(raw_data)

        # Complexity is one less than dependent, but minimum 1
        dependent_complexity = dependent_concept.get("complexity_level", 2)
        complexity = max(1, dependent_complexity - 1)

        # Generate ID
        concept_id = self._generate_id(domain, subfield, term)

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

        return self.store.create(concept)

    def _generate_id(self, domain: str, subfield: str, name: str) -> str:
        """Generate a unique concept ID."""
        name_slug = name.lower().replace(" ", "-")[:20]
        short_uuid = uuid.uuid4().hex[:8]
        return f"{domain.lower()}-{subfield}-{name_slug}-{short_uuid}"
