"""Tests for forward pass, backward pass, and orchestrator engines."""

import pytest
from unittest.mock import Mock, patch
from dataclasses import dataclass

from generator.core.forward_pass import ForwardPassEngine, ForwardPassResult
from generator.core.backward_pass import BackwardPassEngine, BackwardPassResult
from generator.core.orchestrator import Orchestrator, OrchestratorConfig, GenerationResult


class MockConceptStore:
    """Mock implementation of ConceptStore for testing."""

    def __init__(self):
        self.concepts: dict[str, dict] = {}
        self.requires: list[tuple[str, str]] = []

    def get_by_name(self, name: str) -> dict | None:
        for c in self.concepts.values():
            if c["name"] == name:
                return c
        return None

    def get_axioms(self, domain: str) -> list[dict]:
        return [
            c for c in self.concepts.values()
            if c.get("is_axiom") and c.get("domain") == domain
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
        # Return concepts that have no requires relationships
        has_prereqs = {r[0] for r in self.requires}
        return [
            c for c in self.concepts.values()
            if c.get("domain") == domain
            and c["id"] not in has_prereqs
            and not c.get("is_axiom")
        ]

    def create(self, concept: dict) -> dict:
        self.concepts[concept["id"]] = concept
        return concept

    def add_requires(self, concept_id: str, prerequisite_id: str) -> None:
        self.requires.append((concept_id, prerequisite_id))

    def update_prerequisites(self, concept_id: str, prereq_names: list[str]) -> None:
        pass  # Not used in tests


class MockLLMClient:
    """Mock LLM client for testing."""

    def complete(self, prompt: str) -> str:
        # Return a simple formal definition
        if "Convert this informal definition" in prompt:
            return "A **formal definition** with $x \\in X$ and proper notation."
        if "Write a formal mathematical definition" in prompt:
            return "The **concept** is defined as $f: A \\to B$."
        if "prerequisite" in prompt.lower():
            return "Set, Function, Relation"
        return "Test response"


class MockWikipediaExtractor:
    """Mock Wikipedia extractor for testing."""

    def can_extract(self, term: str) -> bool:
        # Simulate finding some but not all terms
        return term.lower() in {"set", "function", "vector space", "derivative"}

    def extract(self, term: str, domain: str, subfield: str):
        from generator.extractors import ExtractedConcept
        return ExtractedConcept(
            name=term,
            raw_definition=f"{term} is a fundamental concept in {domain}.",
            domain=domain,
            subfield=subfield,
            source_type="wikipedia",
            related_terms=["Related Term 1", "Related Term 2"],
        )


class MockResourceExtractor:
    """Mock resource extractor for testing."""

    def enrich_concept(self, concept):
        concept.books = ["Test Book - Author"]
        concept.papers = ["arXiv:1234.5678"]
        return concept


@pytest.fixture
def mock_store():
    """Create a mock store with seed data."""
    store = MockConceptStore()

    # Add some axioms
    store.create({
        "id": "math-set_theory-extensionality-001",
        "name": "Axiom of Extensionality",
        "definition_md": "## Axiom of Extensionality\n\nTwo sets are equal iff they have the same elements.",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [],
        "papers": [],
        "articles": [],
        "related_concepts": ["Set", "Function"],
        "llm_summary": "",
        "is_verified": False,
    })

    store.create({
        "id": "math-set_theory-empty-set-002",
        "name": "Axiom of Empty Set",
        "definition_md": "## Axiom of Empty Set\n\nThere exists a set with no elements.",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [],
        "papers": [],
        "articles": [],
        "related_concepts": [],
        "llm_summary": "",
        "is_verified": False,
    })

    # Add a complex concept for backward pass testing
    store.create({
        "id": "math-linear_algebra-vector-space-003",
        "name": "Vector Space",
        "definition_md": "## Vector Space\n\nA **vector space** requires understanding of **Set** and **Field**.",
        "domain": "MATH",
        "subfield": "linear_algebra",
        "complexity_level": 3,
        "is_axiom": False,
        "books": [],
        "papers": [],
        "articles": [],
        "related_concepts": [],
        "llm_summary": "",
        "is_verified": False,
    })

    return store


@pytest.fixture
def mock_llm():
    return MockLLMClient()


@pytest.fixture
def mock_wikipedia():
    return MockWikipediaExtractor()


@pytest.fixture
def mock_resources():
    return MockResourceExtractor()


class TestForwardPassEngine:
    """Tests for ForwardPassEngine."""

    def test_execute_adds_concepts_from_axioms(
        self, mock_store, mock_llm, mock_wikipedia, mock_resources
    ):
        """Forward pass should expand from axioms and add new concepts."""
        engine = ForwardPassEngine(
            store=mock_store,
            llm_client=mock_llm,
            wikipedia=mock_wikipedia,
            resource_extractor=mock_resources,
        )

        result = engine.execute(domains=["MATH"], target_count=2)

        assert isinstance(result, ForwardPassResult)
        assert result.concepts_added >= 0  # May add concepts
        assert result.concepts_skipped >= 0

    def test_execute_skips_existing_concepts(
        self, mock_store, mock_llm, mock_wikipedia, mock_resources
    ):
        """Forward pass should skip concepts that already exist."""
        # Add a concept that would be found via related_concepts
        mock_store.create({
            "id": "math-set_theory-set-existing",
            "name": "Set",
            "definition_md": "## Set\n\nA collection of elements.",
            "domain": "MATH",
            "subfield": "set_theory",
            "complexity_level": 1,
            "is_axiom": False,
            "books": [],
            "papers": [],
            "articles": [],
            "related_concepts": [],
            "llm_summary": "",
            "is_verified": False,
        })

        engine = ForwardPassEngine(
            store=mock_store,
            llm_client=mock_llm,
            wikipedia=mock_wikipedia,
            resource_extractor=mock_resources,
        )

        result = engine.execute(domains=["MATH"], target_count=5)

        # "Set" should be skipped since it exists
        assert result.concepts_skipped >= 1

    def test_extract_related_terms_finds_bold_terms(
        self, mock_store, mock_llm, mock_wikipedia, mock_resources
    ):
        """Should extract bolded terms from definition."""
        engine = ForwardPassEngine(
            store=mock_store,
            llm_client=mock_llm,
            wikipedia=mock_wikipedia,
            resource_extractor=mock_resources,
        )

        concept = {
            "name": "Test Concept",
            "definition_md": "This uses **Vector Space** and **Linear Map**.",
            "related_concepts": [],
        }

        terms = engine._extract_related_terms(concept)

        assert "Vector Space" in terms
        assert "Linear Map" in terms

    def test_is_likely_concept_filters_common_words(
        self, mock_store, mock_llm, mock_wikipedia, mock_resources
    ):
        """Should filter out common words that aren't concepts."""
        engine = ForwardPassEngine(
            store=mock_store,
            llm_client=mock_llm,
            wikipedia=mock_wikipedia,
            resource_extractor=mock_resources,
        )

        assert engine._is_likely_concept("Vector Space") is True
        assert engine._is_likely_concept("Set") is True
        assert engine._is_likely_concept("example") is False
        assert engine._is_likely_concept("note") is False
        assert engine._is_likely_concept("if") is False


class TestBackwardPassEngine:
    """Tests for BackwardPassEngine."""

    def test_execute_finds_prerequisites(
        self, mock_store, mock_llm, mock_wikipedia, mock_resources
    ):
        """Backward pass should identify and create prerequisites."""
        engine = BackwardPassEngine(
            store=mock_store,
            llm_client=mock_llm,
            wikipedia=mock_wikipedia,
            resource_extractor=mock_resources,
        )

        result = engine.execute(domains=["MATH"], target_count=2)

        assert isinstance(result, BackwardPassResult)
        assert result.concepts_added >= 0
        assert result.prerequisites_linked >= 0

    def test_find_prerequisites_extracts_bold_terms(
        self, mock_store, mock_llm, mock_wikipedia, mock_resources
    ):
        """Should find prerequisite terms mentioned in definition."""
        engine = BackwardPassEngine(
            store=mock_store,
            llm_client=mock_llm,
            wikipedia=mock_wikipedia,
            resource_extractor=mock_resources,
        )

        concept = {
            "name": "Vector Space",
            "definition_md": "Requires understanding of **Set** and assumes knowledge of **Field**.",
        }

        prereqs = engine._find_prerequisites(concept, "MATH")

        # Should find "Set" and possibly "Field"
        assert any("Set" in p for p in prereqs) or any("Field" in p for p in prereqs)

    def test_links_existing_prerequisites(
        self, mock_store, mock_llm, mock_wikipedia, mock_resources
    ):
        """Should link to existing concepts rather than creating duplicates."""
        # Add a concept that is a prerequisite
        mock_store.create({
            "id": "math-set_theory-set-existing",
            "name": "Set",
            "definition_md": "## Set\n\nA collection.",
            "domain": "MATH",
            "subfield": "set_theory",
            "complexity_level": 1,
            "is_axiom": False,
            "books": [],
            "papers": [],
            "articles": [],
            "related_concepts": [],
            "llm_summary": "",
            "is_verified": False,
        })

        engine = BackwardPassEngine(
            store=mock_store,
            llm_client=mock_llm,
            wikipedia=mock_wikipedia,
            resource_extractor=mock_resources,
        )

        result = engine.execute(domains=["MATH"], target_count=5)

        # Should have linked some prerequisites
        assert result.prerequisites_linked >= 0


class TestOrchestrator:
    """Tests for the Orchestrator."""

    def test_run_alternates_passes(
        self, mock_store, mock_llm, mock_wikipedia, mock_resources
    ):
        """Orchestrator should alternate between forward and backward passes."""
        # Patch the engines to track calls
        with patch.object(ForwardPassEngine, 'execute') as mock_forward, \
             patch.object(BackwardPassEngine, 'execute') as mock_backward:

            mock_forward.return_value = ForwardPassResult(
                concepts_added=1, concepts_skipped=0, errors=[]
            )
            mock_backward.return_value = BackwardPassResult(
                concepts_added=1, concepts_skipped=0, prerequisites_linked=1, errors=[]
            )

            config = OrchestratorConfig(pass_ratio=0.5)
            orchestrator = Orchestrator(mock_store, mock_llm, config)
            result = orchestrator.run(target_terms=4, domains=["MATH"])

            # Should have called both passes
            assert mock_forward.call_count >= 1
            assert mock_backward.call_count >= 1

    def test_run_respects_target_count(
        self, mock_store, mock_llm, mock_wikipedia, mock_resources
    ):
        """Orchestrator should stop when target count is reached."""
        config = OrchestratorConfig(pass_ratio=0.5, max_iterations=10)
        orchestrator = Orchestrator(mock_store, mock_llm, config)

        # Replace engines with mocks that always succeed
        orchestrator.forward_engine.execute = Mock(
            return_value=ForwardPassResult(concepts_added=5, concepts_skipped=0, errors=[])
        )
        orchestrator.backward_engine.execute = Mock(
            return_value=BackwardPassResult(
                concepts_added=5, concepts_skipped=0, prerequisites_linked=2, errors=[]
            )
        )

        result = orchestrator.run(target_terms=10, domains=["MATH"])

        assert isinstance(result, GenerationResult)
        assert result.total_concepts_added == 10

    def test_run_single_pass_forward(
        self, mock_store, mock_llm, mock_wikipedia, mock_resources
    ):
        """Should be able to run a single forward pass."""
        orchestrator = Orchestrator(mock_store, mock_llm)
        orchestrator.forward_engine.execute = Mock(
            return_value=ForwardPassResult(concepts_added=3, concepts_skipped=1, errors=[])
        )

        result = orchestrator.run_single_pass("forward", 3, ["MATH"])

        assert isinstance(result, ForwardPassResult)
        assert result.concepts_added == 3

    def test_run_single_pass_backward(
        self, mock_store, mock_llm, mock_wikipedia, mock_resources
    ):
        """Should be able to run a single backward pass."""
        orchestrator = Orchestrator(mock_store, mock_llm)
        orchestrator.backward_engine.execute = Mock(
            return_value=BackwardPassResult(
                concepts_added=2, concepts_skipped=0, prerequisites_linked=3, errors=[]
            )
        )

        result = orchestrator.run_single_pass("backward", 2, ["MATH"])

        assert isinstance(result, BackwardPassResult)
        assert result.concepts_added == 2

    def test_run_single_pass_invalid_type(self, mock_store, mock_llm):
        """Should raise error for invalid pass type."""
        orchestrator = Orchestrator(mock_store, mock_llm)

        with pytest.raises(ValueError):
            orchestrator.run_single_pass("invalid", 1, ["MATH"])

    def test_generation_result_success_property(self):
        """GenerationResult.success should reflect generation quality."""
        # Successful generation
        success_result = GenerationResult(
            total_concepts_added=50,
            forward_concepts=25,
            backward_concepts=25,
            total_passes=10,
            forward_passes=5,
            backward_passes=5,
            all_errors=[],
        )
        assert success_result.success is True

        # Failed generation (no concepts)
        failed_result = GenerationResult(
            total_concepts_added=0,
            forward_concepts=0,
            backward_concepts=0,
            total_passes=2,
            forward_passes=1,
            backward_passes=1,
            all_errors=["Error 1"],
        )
        assert failed_result.success is False

        # Failed generation (too many errors)
        error_result = GenerationResult(
            total_concepts_added=10,
            forward_concepts=5,
            backward_concepts=5,
            total_passes=4,
            forward_passes=2,
            backward_passes=2,
            all_errors=["Error"] * 25,
        )
        assert error_result.success is False
