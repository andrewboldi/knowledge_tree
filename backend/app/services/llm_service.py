"""LLM Service - Kimi K2.5 integration."""


class LLMService:
    """Service for LLM interactions using Kimi K2.5."""

    def __init__(self):
        pass

    async def generate_definition(self, term: str, domain: str) -> str:
        """Generate a formal definition with LaTeX for a term."""
        raise NotImplementedError("LLM definition generation not yet implemented")

    async def formalize_definition(self, informal_def: str, term: str, domain: str) -> str:
        """Formalize an informal definition with proper LaTeX notation."""
        raise NotImplementedError("LLM formalization not yet implemented")
