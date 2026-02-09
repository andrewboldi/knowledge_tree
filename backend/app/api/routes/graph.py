"""Graph API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/tree/{domain}")
async def get_tree(domain: str):
    """Get tree rooted at axioms for a given domain."""
    raise NotImplementedError("Tree retrieval not yet implemented")
