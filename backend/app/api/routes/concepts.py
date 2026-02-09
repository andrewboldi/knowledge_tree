"""Concept API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ...db.concept import Concept, ConceptRepository


router = APIRouter(prefix="/concepts", tags=["concepts"])


class ConceptResponse(BaseModel):
    """Full concept response."""

    id: str
    name: str
    definition_md: str
    domain: str
    subfield: str
    complexity_level: int
    books: list[str]
    papers: list[str]
    articles: list[str]
    related_concepts: list[str]
    llm_summary: str
    is_axiom: bool
    is_verified: bool

    @classmethod
    def from_concept(cls, concept: Concept) -> "ConceptResponse":
        return cls(
            id=concept.id,
            name=concept.name,
            definition_md=concept.definition_md,
            domain=concept.domain,
            subfield=concept.subfield,
            complexity_level=concept.complexity_level,
            books=concept.books,
            papers=concept.papers,
            articles=concept.articles,
            related_concepts=concept.related_concepts,
            llm_summary=concept.llm_summary,
            is_axiom=concept.is_axiom,
            is_verified=concept.is_verified,
        )


class DefinitionResponse(BaseModel):
    """Definition-only response."""

    id: str
    name: str
    definition_md: str


_repo = ConceptRepository()


@router.get("/{concept_id}", response_model=ConceptResponse)
async def get_concept(concept_id: str) -> ConceptResponse:
    """Get a concept by ID with full Markdown definition."""
    concept = _repo.get_by_id(concept_id)
    if concept is None:
        raise HTTPException(status_code=404, detail=f"Concept {concept_id} not found")
    return ConceptResponse.from_concept(concept)


@router.get("/{concept_id}/definition", response_model=DefinitionResponse)
async def get_concept_definition(concept_id: str) -> DefinitionResponse:
    """Get just the Markdown definition for a concept."""
    concept = _repo.get_by_id(concept_id)
    if concept is None:
        raise HTTPException(status_code=404, detail=f"Concept {concept_id} not found")
    return DefinitionResponse(
        id=concept.id,
        name=concept.name,
        definition_md=concept.definition_md,
    )
