"""Tests for MVG service."""

import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.services.llm_service import LLMResponse
from app.services.mvg_service import MVGService, MVGNode, MVGResult


class TestMVGService:
    """Tests for MVGService."""

    @pytest.fixture
    def mock_llm_response(self):
        """Create a mock LLM response."""
        return LLMResponse(
            text=json.dumps({
                "path": [
                    {"name": "Set", "description": "A collection of objects", "is_axiom": True},
                    {"name": "Function", "description": "A mapping between sets", "is_axiom": False},
                    {"name": "Limit", "description": "The value a function approaches", "is_axiom": False},
                    {"name": "Derivative", "description": "Rate of change", "is_axiom": False},
                ],
                "explanation": "This is the minimal path from set theory axioms to derivatives."
            }),
            input_tokens=100,
            output_tokens=50,
        )

    @pytest.fixture
    def mock_llm_response_with_codeblock(self):
        """Create a mock LLM response with markdown code block."""
        return LLMResponse(
            text="```json\n" + json.dumps({
                "path": [
                    {"name": "Set", "description": "A collection", "is_axiom": True},
                ],
                "explanation": "Minimal path."
            }) + "\n```",
            input_tokens=100,
            output_tokens=50,
        )

    @pytest.mark.asyncio
    async def test_generate_basic(self, mock_llm_response):
        """Test basic MVG generation."""
        service = MVGService()

        with patch.object(service._llm, 'generate', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = mock_llm_response

            result = await service.generate("Derivative", "MATH")

            assert result.target == "Derivative"
            assert result.domain == "MATH"
            assert len(result.path) == 4
            assert result.path[0].name == "Set"
            assert result.path[0].is_axiom is True
            assert result.path[3].name == "Derivative"
            assert "minimal path" in result.explanation.lower()

    @pytest.mark.asyncio
    async def test_generate_handles_codeblock(self, mock_llm_response_with_codeblock):
        """Test that MVG generation handles markdown code blocks."""
        service = MVGService()

        with patch.object(service._llm, 'generate', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = mock_llm_response_with_codeblock

            result = await service.generate("Set", "MATH")

            assert result.target == "Set"
            assert len(result.path) == 1
            assert result.path[0].name == "Set"

    @pytest.mark.asyncio
    async def test_generate_invalid_json(self):
        """Test that invalid JSON raises ValueError."""
        service = MVGService()

        with patch.object(service._llm, 'generate', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = LLMResponse(
                text="This is not JSON",
                input_tokens=10,
                output_tokens=5,
            )

            with pytest.raises(ValueError, match="Failed to parse"):
                await service.generate("Test", "MATH")

    @pytest.mark.asyncio
    async def test_generate_empty_path(self):
        """Test handling of empty path in response."""
        service = MVGService()

        with patch.object(service._llm, 'generate', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = LLMResponse(
                text=json.dumps({"path": [], "explanation": "Empty"}),
                input_tokens=10,
                output_tokens=5,
            )

            result = await service.generate("Test", "MATH")

            assert result.path == []
            assert result.explanation == "Empty"

    def test_mvg_node_dataclass(self):
        """Test MVGNode dataclass."""
        node = MVGNode(
            name="Test",
            description="Test description",
            is_axiom=True,
            concept_id="test-001",
        )

        assert node.name == "Test"
        assert node.description == "Test description"
        assert node.is_axiom is True
        assert node.concept_id == "test-001"

    def test_mvg_node_defaults(self):
        """Test MVGNode default values."""
        node = MVGNode(name="Test", description="Desc")

        assert node.is_axiom is False
        assert node.concept_id is None

    def test_mvg_result_dataclass(self):
        """Test MVGResult dataclass."""
        result = MVGResult(
            target="Derivative",
            domain="MATH",
            path=[MVGNode(name="Set", description="Collection")],
            explanation="Test explanation",
        )

        assert result.target == "Derivative"
        assert result.domain == "MATH"
        assert len(result.path) == 1
        assert result.explanation == "Test explanation"
