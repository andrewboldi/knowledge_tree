"""Contribution model and repository for Neo4j."""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .neo4j_client import get_client


@dataclass
class Contribution:
    """User contribution to the Knowledge Tree."""

    id: str
    user_id: str  # Firebase UID
    concept_id: str
    contribution_type: str  # "concept", "book", "paper", "article"
    created_at: str  # ISO format timestamp
    user_email: Optional[str] = None
    user_display_name: Optional[str] = None


class ContributionRepository:
    """Repository for Contribution CRUD operations."""

    def create(self, contribution: Contribution) -> Contribution:
        """Create a new Contribution node and link to concept."""
        client = get_client()
        query = """
        MATCH (c:Concept {id: $concept_id})
        CREATE (contrib:Contribution {
            id: $id,
            user_id: $user_id,
            concept_id: $concept_id,
            contribution_type: $contribution_type,
            created_at: $created_at,
            user_email: $user_email,
            user_display_name: $user_display_name
        })
        CREATE (contrib)-[:CONTRIBUTED_TO]->(c)
        RETURN contrib
        """
        client.execute_query(
            query,
            {
                "id": contribution.id,
                "user_id": contribution.user_id,
                "concept_id": contribution.concept_id,
                "contribution_type": contribution.contribution_type,
                "created_at": contribution.created_at,
                "user_email": contribution.user_email,
                "user_display_name": contribution.user_display_name,
            },
        )
        return contribution

    def get_by_user(self, user_id: str) -> list[Contribution]:
        """Get all contributions by a user."""
        client = get_client()
        query = """
        MATCH (contrib:Contribution {user_id: $user_id})
        RETURN contrib
        ORDER BY contrib.created_at DESC
        """
        results = client.execute_query(query, {"user_id": user_id})
        return [Contribution(**r["contrib"]) for r in results]

    def get_by_concept(self, concept_id: str) -> list[Contribution]:
        """Get all contributions for a concept."""
        client = get_client()
        query = """
        MATCH (contrib:Contribution {concept_id: $concept_id})
        RETURN contrib
        ORDER BY contrib.created_at DESC
        """
        results = client.execute_query(query, {"concept_id": concept_id})
        return [Contribution(**r["contrib"]) for r in results]


def generate_contribution_id() -> str:
    """Generate a unique contribution ID."""
    return f"contrib-{uuid.uuid4().hex[:12]}"


def create_contribution_from_user(
    user_id: str,
    concept_id: str,
    contribution_type: str,
    user_email: Optional[str] = None,
    user_display_name: Optional[str] = None,
) -> Contribution:
    """Factory function to create a Contribution with generated ID and timestamp."""
    return Contribution(
        id=generate_contribution_id(),
        user_id=user_id,
        concept_id=concept_id,
        contribution_type=contribution_type,
        created_at=datetime.utcnow().isoformat(),
        user_email=user_email,
        user_display_name=user_display_name,
    )
