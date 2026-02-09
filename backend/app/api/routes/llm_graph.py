"""LLM/MVG API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/mvg", tags=["mvg"])


@router.post("/generate")
async def generate_mvg():
    """Generate minimum viable graph for a target topic."""
    raise NotImplementedError("MVG generation not yet implemented")
