"""Concept API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/concepts", tags=["concepts"])


@router.get("/{concept_id}")
async def get_concept(concept_id: str):
    """Get concept with full Markdown definition."""
    raise NotImplementedError("Concept retrieval not yet implemented")


@router.get("/{concept_id}/definition")
async def get_concept_definition(concept_id: str):
    """Get just the Markdown definition for a concept."""
    raise NotImplementedError("Definition retrieval not yet implemented")
