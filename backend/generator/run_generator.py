#!/usr/bin/env python3
"""Knowledge Tree Generator CLI.

This script runs the knowledge generator to populate the graph database
with formal definitions across all domains.

Usage:
    python -m generator.run_generator --domains MATH PHYSICS --target 100
    python -m generator.run_generator --all-domains --target 500
    python -m generator.run_generator --seed-only  # Just load seed definitions
"""

import argparse
import logging
import sys
from dataclasses import dataclass, field
from typing import Protocol

from .seeds import DOMAIN_SEEDS
from .core import Orchestrator, OrchestratorConfig, GenerationResult


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# All available domains
ALL_DOMAINS = ["MATH", "PHYSICS", "CHEMISTRY", "BIOLOGY", "CS"]


class ConceptRepository(Protocol):
    """Protocol for concept storage."""

    def get_by_name(self, name: str) -> dict | None:
        ...

    def get_axioms(self, domain: str) -> list[dict]:
        ...

    def get_by_complexity_range(
        self, domain: str, min_level: int, max_level: int
    ) -> list[dict]:
        ...

    def get_complex_concepts(self, domain: str, min_level: int) -> list[dict]:
        ...

    def get_incomplete_concepts(self, domain: str) -> list[dict]:
        ...

    def create(self, concept: dict) -> dict:
        ...

    def add_requires(self, concept_id: str, prerequisite_id: str) -> None:
        ...

    def update_prerequisites(self, concept_id: str, prereq_names: list[str]) -> None:
        ...


@dataclass
class InMemoryConceptStore:
    """Simple in-memory concept store for testing/dry-run mode."""

    concepts: dict[str, dict] = field(default_factory=dict)
    concepts_by_name: dict[str, dict] = field(default_factory=dict)
    relationships: list[tuple[str, str]] = field(default_factory=list)

    def get_by_name(self, name: str) -> dict | None:
        return self.concepts_by_name.get(name.lower())

    def get_axioms(self, domain: str) -> list[dict]:
        return [
            c for c in self.concepts.values()
            if c.get("domain") == domain and c.get("is_axiom", False)
        ]

    def get_by_complexity_range(
        self, domain: str, min_level: int, max_level: int
    ) -> list[dict]:
        return [
            c for c in self.concepts.values()
            if c.get("domain") == domain
            and min_level <= c.get("complexity_level", 0) <= max_level
        ]

    def get_complex_concepts(self, domain: str, min_level: int) -> list[dict]:
        return [
            c for c in self.concepts.values()
            if c.get("domain") == domain
            and c.get("complexity_level", 0) >= min_level
        ]

    def get_incomplete_concepts(self, domain: str) -> list[dict]:
        # For simplicity, return concepts that have prerequisites listed but not linked
        return []

    def create(self, concept: dict) -> dict:
        concept_id = concept.get("id", f"concept-{len(self.concepts)}")
        concept["id"] = concept_id
        self.concepts[concept_id] = concept
        self.concepts_by_name[concept["name"].lower()] = concept
        return concept

    def add_requires(self, concept_id: str, prerequisite_id: str) -> None:
        self.relationships.append((concept_id, prerequisite_id))

    def update_prerequisites(self, concept_id: str, prereq_names: list[str]) -> None:
        pass  # In-memory store doesn't track this separately


def load_seed_definitions(store: ConceptRepository, domains: list[str]) -> int:
    """Load seed definitions for specified domains.

    Args:
        store: The concept repository to load into
        domains: List of domain names to load

    Returns:
        Number of seed concepts loaded
    """
    loaded = 0

    for domain in domains:
        seeds = DOMAIN_SEEDS.get(domain, [])
        logger.info(f"Loading {len(seeds)} seed definitions for {domain}")

        for seed in seeds:
            name = seed["name"]
            if store.get_by_name(name):
                logger.debug(f"Seed '{name}' already exists, skipping")
                continue

            # Create concept from seed
            concept = {
                "id": f"{domain.lower()}-seed-{name.lower().replace(' ', '-')}",
                "name": name,
                "definition_md": seed["definition_md"],
                "domain": domain,
                "subfield": seed.get("subfield", "general"),
                "complexity_level": seed.get("complexity_level", 0),
                "is_axiom": seed.get("is_axiom", False),
                "is_verified": True,  # Seeds are pre-verified
                "books": seed.get("books", []),
                "papers": seed.get("papers", []),
                "articles": [],
                "related_concepts": [],
                "llm_summary": "",
            }

            created = store.create(concept)
            loaded += 1
            logger.debug(f"Loaded seed: {name}")

            # Link prerequisites
            for prereq_name in seed.get("prerequisites", []):
                prereq = store.get_by_name(prereq_name)
                if prereq:
                    store.add_requires(created["id"], prereq["id"])

    return loaded


def run_generator(
    store: ConceptRepository,
    domains: list[str],
    target_count: int,
    load_seeds: bool = True,
) -> GenerationResult:
    """Run the knowledge generator.

    Args:
        store: The concept repository
        domains: Domains to generate for
        target_count: Target number of new concepts
        load_seeds: Whether to load seed definitions first

    Returns:
        GenerationResult with statistics
    """
    # Load seeds first
    if load_seeds:
        seed_count = load_seed_definitions(store, domains)
        logger.info(f"Loaded {seed_count} seed definitions")

    # Configure and run orchestrator
    config = OrchestratorConfig(
        domains=domains,
        pass_ratio=0.10,
        forward_max_complexity=3,
        backward_min_complexity=2,
        max_iterations=100,
    )

    orchestrator = Orchestrator(store=store, config=config)

    logger.info(f"Starting generation: target={target_count}, domains={domains}")
    result = orchestrator.run(target_terms=target_count, domains=domains)

    return result


def print_summary(result: GenerationResult, store: InMemoryConceptStore | None = None):
    """Print generation summary."""
    print("\n" + "=" * 60)
    print("GENERATION SUMMARY")
    print("=" * 60)
    print(f"Total concepts added: {result.total_concepts_added}")
    print(f"  Forward pass: {result.forward_concepts}")
    print(f"  Backward pass: {result.backward_concepts}")
    print(f"Total passes: {result.total_passes}")
    print(f"  Forward: {result.forward_passes}")
    print(f"  Backward: {result.backward_passes}")

    if result.all_errors:
        print(f"\nErrors ({len(result.all_errors)}):")
        for err in result.all_errors[:10]:
            print(f"  - {err}")
        if len(result.all_errors) > 10:
            print(f"  ... and {len(result.all_errors) - 10} more")

    print(f"\nSuccess: {result.success}")

    if store:
        print(f"\nTotal concepts in store: {len(store.concepts)}")
        print(f"Total relationships: {len(store.relationships)}")

        # Domain breakdown
        print("\nConcepts by domain:")
        domain_counts = {}
        for concept in store.concepts.values():
            domain = concept.get("domain", "UNKNOWN")
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        for domain, count in sorted(domain_counts.items()):
            print(f"  {domain}: {count}")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Run the Knowledge Tree generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m generator.run_generator --domains MATH --target 50
  python -m generator.run_generator --all-domains --target 200
  python -m generator.run_generator --seed-only
  python -m generator.run_generator --dry-run --all-domains --target 100
        """,
    )

    parser.add_argument(
        "--domains",
        nargs="+",
        choices=ALL_DOMAINS,
        help="Domains to generate (default: MATH)",
    )
    parser.add_argument(
        "--all-domains",
        action="store_true",
        help="Generate for all domains",
    )
    parser.add_argument(
        "--target",
        type=int,
        default=50,
        help="Target number of new concepts to generate (default: 50)",
    )
    parser.add_argument(
        "--seed-only",
        action="store_true",
        help="Only load seed definitions, don't run generator",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Use in-memory store instead of database",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Determine domains
    if args.all_domains:
        domains = ALL_DOMAINS
    elif args.domains:
        domains = args.domains
    else:
        domains = ["MATH"]

    logger.info(f"Domains: {domains}")

    # Get or create store
    if args.dry_run:
        logger.info("Running in dry-run mode with in-memory store")
        store = InMemoryConceptStore()
    else:
        # Try to import the real repository
        try:
            from app.db.concept import get_concept_repository
            store = get_concept_repository()
            logger.info("Using Neo4j concept repository")
        except ImportError as e:
            logger.warning(f"Could not import database repository: {e}")
            logger.info("Falling back to in-memory store")
            store = InMemoryConceptStore()

    # Run
    if args.seed_only:
        count = load_seed_definitions(store, domains)
        print(f"\nLoaded {count} seed definitions")
        if isinstance(store, InMemoryConceptStore):
            print(f"Total concepts in store: {len(store.concepts)}")
    else:
        result = run_generator(
            store=store,
            domains=domains,
            target_count=args.target,
            load_seeds=True,
        )
        print_summary(
            result,
            store if isinstance(store, InMemoryConceptStore) else None,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
