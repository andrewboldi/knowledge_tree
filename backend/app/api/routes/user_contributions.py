"""User contribution API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/contributions", tags=["contributions"])


@router.post("/concept")
async def add_concept():
    """Add new definition (Markdown + LaTeX). Requires auth."""
    raise NotImplementedError("Concept creation not yet implemented")


@router.post("/{concept_id}/resource")
async def add_resource(concept_id: str):
    """Add book/paper to a concept. Requires auth."""
    raise NotImplementedError("Resource addition not yet implemented")
