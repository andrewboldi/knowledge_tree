"""Minimum Viable Graph Service."""


class MVGService:
    """Service for generating minimum viable graphs (learning paths)."""

    def __init__(self):
        pass

    async def generate_mvg(self, target_concept: str, user_knowledge: list[str] | None = None) -> dict:
        """Generate minimum viable graph from current knowledge to target concept."""
        raise NotImplementedError("MVG generation not yet implemented")
