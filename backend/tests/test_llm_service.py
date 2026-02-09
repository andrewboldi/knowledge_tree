"""Tests for LLM service."""

import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.services.llm_service import LLMService, LLMResponse, get_llm_service


class TestLLMService:
    """Tests for LLMService."""

    def test_init_default_model(self):
        """Test default model initialization."""
        service = LLMService()
        assert service.model == "opencode/kimi-k2.5"

    def test_init_custom_model(self):
        """Test custom model initialization."""
        service = LLMService(model="opencode/gpt-5")
        assert service.model == "opencode/gpt-5"

    @pytest.mark.asyncio
    async def test_generate_success(self):
        """Test successful generation."""
        service = LLMService()

        mock_stdout = "\n".join([
            json.dumps({"type": "step_start", "timestamp": 1}),
            json.dumps({"type": "text", "part": {"text": "Hello, "}}),
            json.dumps({"type": "text", "part": {"text": "world!"}}),
            json.dumps({
                "type": "step_finish",
                "part": {"tokens": {"input": 100, "output": 50}}
            }),
        ]).encode()

        mock_process = AsyncMock()
        mock_process.returncode = 0
        mock_process.communicate = AsyncMock(return_value=(mock_stdout, b""))

        with patch("asyncio.create_subprocess_exec", return_value=mock_process):
            result = await service.generate("Test prompt")

            assert result.text == "Hello, world!"
            assert result.input_tokens == 100
            assert result.output_tokens == 50

    @pytest.mark.asyncio
    async def test_generate_failure(self):
        """Test generation failure."""
        service = LLMService()

        mock_process = AsyncMock()
        mock_process.returncode = 1
        mock_process.communicate = AsyncMock(return_value=(b"", b"Error message"))

        with patch("asyncio.create_subprocess_exec", return_value=mock_process):
            with pytest.raises(RuntimeError, match="opencode failed"):
                await service.generate("Test prompt")

    @pytest.mark.asyncio
    async def test_generate_no_text(self):
        """Test generation with no text response."""
        service = LLMService()

        mock_stdout = json.dumps({"type": "step_start", "timestamp": 1}).encode()

        mock_process = AsyncMock()
        mock_process.returncode = 0
        mock_process.communicate = AsyncMock(return_value=(mock_stdout, b""))

        with patch("asyncio.create_subprocess_exec", return_value=mock_process):
            with pytest.raises(RuntimeError, match="No text response"):
                await service.generate("Test prompt")

    def test_llm_response_dataclass(self):
        """Test LLMResponse dataclass."""
        response = LLMResponse(
            text="Test response",
            input_tokens=100,
            output_tokens=50,
        )

        assert response.text == "Test response"
        assert response.input_tokens == 100
        assert response.output_tokens == 50

    def test_get_llm_service_singleton(self):
        """Test that get_llm_service returns singleton."""
        # Reset global singleton for test
        import app.services.llm_service as module
        module._llm_service = None

        service1 = get_llm_service()
        service2 = get_llm_service()

        assert service1 is service2
