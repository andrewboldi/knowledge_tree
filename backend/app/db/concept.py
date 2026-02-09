"""Concept model and repository for Neo4j."""

import uuid
from dataclasses import dataclass, field
from typing import Optional

from .neo4j_client import get_client


@dataclass
class Concept:
    """Knowledge Tree Concept node."""

    id: str
    name: str
    definition_md: str
    domain: str  # MATH, PHYSICS, CHEMISTRY, BIOLOGY, CS
    subfield: str
    complexity_level: int  # 0 = axiom, higher = more complex
    books: list[str] = field(default_factory=list)
    papers: list[str] = field(default_factory=list)
    articles: list[str] = field(default_factory=list)
    related_concepts: list[str] = field(default_factory=list)
    llm_summary: str = ""
    is_axiom: bool = False
    is_verified: bool = False


class ConceptRepository:
    """Repository for Concept CRUD operations."""

    def create(self, concept: Concept) -> Concept:
        """Create a new Concept node."""
        client = get_client()
        query = """
        CREATE (c:Concept {
            id: $id,
            name: $name,
            definition_md: $definition_md,
            domain: $domain,
            subfield: $subfield,
            complexity_level: $complexity_level,
            books: $books,
            papers: $papers,
            articles: $articles,
            related_concepts: $related_concepts,
            llm_summary: $llm_summary,
            is_axiom: $is_axiom,
            is_verified: $is_verified
        })
        RETURN c
        """
        client.execute_query(
            query,
            {
                "id": concept.id,
                "name": concept.name,
                "definition_md": concept.definition_md,
                "domain": concept.domain,
                "subfield": concept.subfield,
                "complexity_level": concept.complexity_level,
                "books": concept.books,
                "papers": concept.papers,
                "articles": concept.articles,
                "related_concepts": concept.related_concepts,
                "llm_summary": concept.llm_summary,
                "is_axiom": concept.is_axiom,
                "is_verified": concept.is_verified,
            },
        )
        return concept

    def get_by_id(self, concept_id: str) -> Optional[Concept]:
        """Get a Concept by ID."""
        client = get_client()
        query = "MATCH (c:Concept {id: $id}) RETURN c"
        results = client.execute_query(query, {"id": concept_id})
        if not results:
            return None
        data = results[0]["c"]
        return Concept(**data)

    def get_by_domain(self, domain: str) -> list[Concept]:
        """Get all Concepts in a domain."""
        client = get_client()
        query = "MATCH (c:Concept {domain: $domain}) RETURN c ORDER BY c.complexity_level"
        results = client.execute_query(query, {"domain": domain})
        return [Concept(**r["c"]) for r in results]

    def get_axioms(self, domain: Optional[str] = None) -> list[Concept]:
        """Get all axiom Concepts, optionally filtered by domain."""
        client = get_client()
        if domain:
            query = "MATCH (c:Concept {is_axiom: true, domain: $domain}) RETURN c"
            results = client.execute_query(query, {"domain": domain})
        else:
            query = "MATCH (c:Concept {is_axiom: true}) RETURN c"
            results = client.execute_query(query)
        return [Concept(**r["c"]) for r in results]

    def add_requires(self, concept_id: str, prerequisite_id: str) -> None:
        """Add a REQUIRES relationship between concepts."""
        client = get_client()
        query = """
        MATCH (c:Concept {id: $concept_id})
        MATCH (p:Concept {id: $prerequisite_id})
        MERGE (c)-[:REQUIRES]->(p)
        """
        client.execute_query(
            query, {"concept_id": concept_id, "prerequisite_id": prerequisite_id}
        )

    def get_prerequisites(self, concept_id: str) -> list[Concept]:
        """Get all prerequisites for a concept."""
        client = get_client()
        query = """
        MATCH (c:Concept {id: $id})-[:REQUIRES]->(p:Concept)
        RETURN p
        """
        results = client.execute_query(query, {"id": concept_id})
        return [Concept(**r["p"]) for r in results]

    def get_dependents(self, concept_id: str) -> list[Concept]:
        """Get all concepts that require this concept."""
        client = get_client()
        query = """
        MATCH (c:Concept)-[:REQUIRES]->(p:Concept {id: $id})
        RETURN c
        """
        results = client.execute_query(query, {"id": concept_id})
        return [Concept(**r["c"]) for r in results]

    def delete(self, concept_id: str) -> None:
        """Delete a Concept and its relationships."""
        client = get_client()
        query = "MATCH (c:Concept {id: $id}) DETACH DELETE c"
        client.execute_query(query, {"id": concept_id})


def generate_concept_id(domain: str, subfield: str, name: str) -> str:
    """Generate a concept ID following the naming convention."""
    name_slug = name.lower().replace(" ", "-")[:20]
    short_uuid = uuid.uuid4().hex[:8]
    return f"{domain.lower()}-{subfield}-{name_slug}-{short_uuid}"
