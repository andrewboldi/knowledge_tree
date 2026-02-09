"""Orchestrator for the knowledge generation algorithm.

Implements the alternating pass algorithm:
- 10% forward pass (expand from axioms)
- 10% backward pass (trace prerequisites)
- Repeat until target count reached

Each pass extracts formal definitions with LaTeX notation.
"""

import logging
from dataclasses import dataclass, field
from typing import Protocol

from .forward_pass import ForwardPassEngine, ForwardPassResult
from .backward_pass import BackwardPassEngine, BackwardPassResult
from .definition_formatter import DefinitionFormatter, LLMClient
from ..extractors import WikipediaExtractor, ResourceExtractor


logger = logging.getLogger(__name__)


class ConceptRepository(Protocol):
    """Protocol for concept storage - matches the app's ConceptRepository."""

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

    def get_complex_concepts(self, domain: str, min_level: int) -> list[dict]:
        """Get concepts at or above a complexity level."""
        ...

    def get_incomplete_concepts(self, domain: str) -> list[dict]:
        """Get concepts with unresolved prerequisites."""
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
class OrchestratorConfig:
    """Configuration for the orchestrator."""

    # Pass ratio (percentage of target for each pass)
    pass_ratio: float = 0.10  # 10% per pass

    # Domain settings
    domains: list[str] = field(default_factory=lambda: ["MATH"])

    # Complexity bounds
    forward_max_complexity: int = 3  # Max complexity to expand from in forward
    backward_min_complexity: int = 2  # Min complexity to trace back from

    # Safety limits
    max_iterations: int = 100  # Maximum number of pass iterations
    max_errors_per_pass: int = 10  # Abort pass if too many errors


@dataclass
class GenerationResult:
    """Result of a full generation run."""

    total_concepts_added: int
    forward_concepts: int
    backward_concepts: int
    total_passes: int
    forward_passes: int
    backward_passes: int
    all_errors: list[str]

    @property
    def success(self) -> bool:
        """Check if generation was successful (added concepts with few errors)."""
        return self.total_concepts_added > 0 and len(self.all_errors) < 20


class Orchestrator:
    """Main orchestrator for knowledge generation.

    Alternates between forward and backward passes to build a comprehensive
    knowledge graph. Each pass adds concepts and links them via prerequisites.

    Usage:
        store = get_concept_repository()  # Your storage implementation
        orchestrator = Orchestrator(store)
        result = orchestrator.run(target_terms=100, domains=["MATH"])
    """

    def __init__(
        self,
        store: ConceptRepository,
        llm_client: LLMClient | None = None,
        config: OrchestratorConfig | None = None,
    ):
        self.store = store
        self.config = config or OrchestratorConfig()

        # Initialize shared components
        self.wikipedia = WikipediaExtractor()
        self.resource_extractor = ResourceExtractor()
        self.formatter = DefinitionFormatter(llm_client)

        # Initialize pass engines
        self.forward_engine = ForwardPassEngine(
            store=store,
            llm_client=llm_client,
            wikipedia=self.wikipedia,
            resource_extractor=self.resource_extractor,
            formatter=self.formatter,
        )
        self.backward_engine = BackwardPassEngine(
            store=store,
            llm_client=llm_client,
            wikipedia=self.wikipedia,
            resource_extractor=self.resource_extractor,
            formatter=self.formatter,
        )

    def run(
        self,
        target_terms: int,
        domains: list[str] | None = None,
    ) -> GenerationResult:
        """Run the alternating pass algorithm.

        Alternates between forward (expand from axioms) and backward
        (trace prerequisites) passes, each adding ~10% of the target.

        Args:
            target_terms: Total number of new concepts to generate
            domains: Domains to generate for (defaults to config)

        Returns:
            GenerationResult with statistics
        """
        domains = domains or self.config.domains
        batch_size = int(target_terms * self.config.pass_ratio)
        batch_size = max(1, batch_size)  # At least 1 per pass

        current = 0
        pass_type = "forward"
        iteration = 0

        forward_total = 0
        backward_total = 0
        forward_passes = 0
        backward_passes = 0
        all_errors: list[str] = []

        logger.info(
            f"Starting generation: target={target_terms}, "
            f"batch_size={batch_size}, domains={domains}"
        )

        while current < target_terms and iteration < self.config.max_iterations:
            terms_this_batch = min(batch_size, target_terms - current)

            if pass_type == "forward":
                result = self._execute_forward_pass(domains, terms_this_batch)
                added = result.concepts_added
                forward_total += added
                forward_passes += 1
                all_errors.extend(result.errors)
                pass_type = "backward"

                logger.info(
                    f"Forward pass #{forward_passes}: added={added}, "
                    f"skipped={result.concepts_skipped}"
                )
            else:
                result = self._execute_backward_pass(domains, terms_this_batch)
                added = result.concepts_added
                backward_total += added
                backward_passes += 1
                all_errors.extend(result.errors)
                pass_type = "forward"

                logger.info(
                    f"Backward pass #{backward_passes}: added={added}, "
                    f"linked={result.prerequisites_linked}"
                )

            current += added
            iteration += 1

            # Check for stall (no progress)
            if added == 0:
                logger.warning(f"Pass produced no new concepts, continuing...")

            logger.info(
                f"Progress: {current}/{target_terms} concepts "
                f"({100*current/target_terms:.1f}%)"
            )

        total_passes = forward_passes + backward_passes
        logger.info(
            f"Generation complete: {current} concepts in {total_passes} passes "
            f"(forward={forward_total}, backward={backward_total})"
        )

        return GenerationResult(
            total_concepts_added=current,
            forward_concepts=forward_total,
            backward_concepts=backward_total,
            total_passes=total_passes,
            forward_passes=forward_passes,
            backward_passes=backward_passes,
            all_errors=all_errors,
        )

    def _execute_forward_pass(
        self, domains: list[str], target_count: int
    ) -> ForwardPassResult:
        """Execute a single forward pass."""
        return self.forward_engine.execute(
            domains=domains,
            target_count=target_count,
            max_complexity=self.config.forward_max_complexity,
        )

    def _execute_backward_pass(
        self, domains: list[str], target_count: int
    ) -> BackwardPassResult:
        """Execute a single backward pass."""
        return self.backward_engine.execute(
            domains=domains,
            target_count=target_count,
            min_complexity=self.config.backward_min_complexity,
        )

    def run_single_pass(
        self,
        pass_type: str,
        target_count: int,
        domains: list[str] | None = None,
    ) -> ForwardPassResult | BackwardPassResult:
        """Run a single pass of the specified type.

        Useful for testing or targeted generation.

        Args:
            pass_type: "forward" or "backward"
            target_count: Number of concepts to add
            domains: Domains to generate for

        Returns:
            ForwardPassResult or BackwardPassResult
        """
        domains = domains or self.config.domains

        if pass_type == "forward":
            return self._execute_forward_pass(domains, target_count)
        elif pass_type == "backward":
            return self._execute_backward_pass(domains, target_count)
        else:
            raise ValueError(f"Unknown pass type: {pass_type}")
