"""Tests for user contribution endpoints."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.auth.firebase_auth import FirebaseUser
from app.db.concept import Concept


# Mock user for authenticated requests
mock_user = FirebaseUser(
    uid="test-user-123",
    email="test@example.com",
    email_verified=True,
    display_name="Test User",
)


def override_get_current_user():
    """Override auth dependency for testing."""
    return mock_user


@pytest.fixture
def client():
    """Create test client with auth override."""
    from app.api.routes.user_contributions import router
    from app.auth.firebase_auth import get_current_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestCreateConcept:
    """Tests for POST /api/contributions/concept."""

    def test_create_concept_requires_auth(self):
        """Test that creating a concept requires authentication."""
        # Without auth override
        app.dependency_overrides.clear()
        client = TestClient(app)
        response = client.post(
            "/api/contributions/concept",
            json={
                "name": "Test Concept",
                "definition_md": "A test definition",
                "domain": "MATH",
                "subfield": "test",
            },
        )
        assert response.status_code == 401

    def test_create_concept_invalid_domain(self, client):
        """Test that invalid domains are rejected."""
        response = client.post(
            "/api/contributions/concept",
            json={
                "name": "Test Concept",
                "definition_md": "A test definition",
                "domain": "INVALID",
                "subfield": "test",
            },
        )
        assert response.status_code == 400
        assert "Invalid domain" in response.json()["detail"]

    def test_create_concept_negative_complexity(self, client):
        """Test that negative complexity levels are rejected."""
        response = client.post(
            "/api/contributions/concept",
            json={
                "name": "Test Concept",
                "definition_md": "A test definition",
                "domain": "MATH",
                "subfield": "test",
                "complexity_level": -1,
            },
        )
        assert response.status_code == 400
        assert "Complexity level" in response.json()["detail"]

    @patch("app.api.routes.user_contributions._concept_repo")
    @patch("app.api.routes.user_contributions._contribution_repo")
    def test_create_concept_success(self, mock_contrib_repo, mock_concept_repo, client):
        """Test successful concept creation."""
        mock_concept_repo.create.return_value = MagicMock()
        mock_concept_repo.get_by_id.return_value = None
        mock_contrib_repo.create.return_value = MagicMock()

        response = client.post(
            "/api/contributions/concept",
            json={
                "name": "Vector Space",
                "definition_md": "## Vector Space\n\nA **vector space** over $F$...",
                "domain": "MATH",
                "subfield": "linear_algebra",
                "complexity_level": 2,
                "books": ["Linear Algebra Done Right - Axler"],
                "papers": [],
                "prerequisite_ids": [],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "concept_id" in data
        assert "contribution_id" in data
        assert "Vector Space" in data["message"]


class TestAddResource:
    """Tests for POST /api/contributions/{concept_id}/resource."""

    def test_add_resource_requires_auth(self):
        """Test that adding a resource requires authentication."""
        app.dependency_overrides.clear()
        client = TestClient(app)
        response = client.post(
            "/api/contributions/test-concept/resource",
            json={
                "resource_type": "book",
                "resource": "Test Book - Author",
            },
        )
        assert response.status_code == 401

    def test_add_resource_invalid_type(self, client):
        """Test that invalid resource types are rejected."""
        response = client.post(
            "/api/contributions/test-concept/resource",
            json={
                "resource_type": "invalid",
                "resource": "Test Resource",
            },
        )
        assert response.status_code == 400
        assert "Invalid resource type" in response.json()["detail"]

    @patch("app.api.routes.user_contributions._concept_repo")
    def test_add_resource_concept_not_found(self, mock_concept_repo, client):
        """Test adding resource to non-existent concept."""
        mock_concept_repo.get_by_id.return_value = None

        response = client.post(
            "/api/contributions/nonexistent/resource",
            json={
                "resource_type": "book",
                "resource": "Test Book",
            },
        )
        assert response.status_code == 404

    @patch("app.api.routes.user_contributions._concept_repo")
    @patch("app.api.routes.user_contributions._contribution_repo")
    @patch("app.api.routes.user_contributions.get_client")
    def test_add_book_success(self, mock_get_client, mock_contrib_repo, mock_concept_repo, client):
        """Test successfully adding a book."""
        mock_concept = Concept(
            id="math-linalg-vector-123",
            name="Vector Space",
            definition_md="Test",
            domain="MATH",
            subfield="linear_algebra",
            complexity_level=2,
        )
        mock_concept_repo.get_by_id.return_value = mock_concept
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_contrib_repo.create.return_value = MagicMock()

        response = client.post(
            "/api/contributions/math-linalg-vector-123/resource",
            json={
                "resource_type": "book",
                "resource": "Linear Algebra Done Right - Axler, Ch. 1",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["resource_type"] == "book"
        assert "contribution_id" in data
