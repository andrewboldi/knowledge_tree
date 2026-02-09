"""Tests for MVG API endpoints."""

import json
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.services.mvg_service import MVGResult, MVGNode


@pytest.fixture
def client():
    """Create a test client."""
    # Disable Neo4j initialization for tests
    with patch("app.main.get_client"):
        yield TestClient(app)


class TestMVGAPI:
    """Tests for MVG API endpoints."""

    @pytest.fixture
    def mock_mvg_result(self):
        """Create a mock MVG result."""
        return MVGResult(
            target="Derivative",
            domain="MATH",
            path=[
                MVGNode(name="Set", description="A collection", is_axiom=True),
                MVGNode(name="Limit", description="Approaching value", is_axiom=False),
                MVGNode(name="Derivative", description="Rate of change", is_axiom=False),
            ],
            explanation="Minimal path to understand derivatives.",
        )

    def test_generate_mvg_success(self, client, mock_mvg_result):
        """Test successful MVG generation."""
        with patch("app.api.routes.mvg.get_mvg_service") as mock_service:
            mock_instance = mock_service.return_value
            mock_instance.generate = AsyncMock(return_value=mock_mvg_result)

            response = client.post(
                "/api/mvg/generate",
                json={"target": "Derivative", "domain": "MATH"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["target"] == "Derivative"
            assert data["domain"] == "MATH"
            assert len(data["path"]) == 3
            assert data["path"][0]["name"] == "Set"
            assert data["path"][0]["is_axiom"] is True
            assert "explanation" in data

    def test_generate_mvg_default_domain(self, client, mock_mvg_result):
        """Test MVG generation with default domain."""
        with patch("app.api.routes.mvg.get_mvg_service") as mock_service:
            mock_instance = mock_service.return_value
            mock_instance.generate = AsyncMock(return_value=mock_mvg_result)

            response = client.post(
                "/api/mvg/generate",
                json={"target": "Derivative"},
            )

            assert response.status_code == 200
            # Verify domain defaulted to MATH
            mock_instance.generate.assert_called_once_with(
                target="Derivative", domain="MATH"
            )

    def test_generate_mvg_parse_error(self, client):
        """Test MVG generation with parse error."""
        with patch("app.api.routes.mvg.get_mvg_service") as mock_service:
            mock_instance = mock_service.return_value
            mock_instance.generate = AsyncMock(
                side_effect=ValueError("Failed to parse LLM response")
            )

            response = client.post(
                "/api/mvg/generate",
                json={"target": "Derivative"},
            )

            assert response.status_code == 422
            assert "Failed to parse" in response.json()["detail"]

    def test_generate_mvg_llm_error(self, client):
        """Test MVG generation with LLM service error."""
        with patch("app.api.routes.mvg.get_mvg_service") as mock_service:
            mock_instance = mock_service.return_value
            mock_instance.generate = AsyncMock(
                side_effect=RuntimeError("opencode failed")
            )

            response = client.post(
                "/api/mvg/generate",
                json={"target": "Derivative"},
            )

            assert response.status_code == 503
            assert "LLM service error" in response.json()["detail"]

    def test_generate_mvg_missing_target(self, client):
        """Test MVG generation with missing target."""
        response = client.post(
            "/api/mvg/generate",
            json={"domain": "MATH"},
        )

        assert response.status_code == 422  # Validation error
