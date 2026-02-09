"""Minimum Viable Graph (MVG) service.

Generates minimal learning paths from axioms to target concepts using LLM.
"""

import json
import re
from dataclasses import dataclass

from .llm_service import get_llm_service
from ..db.concept import Concept, ConceptRepository


@dataclass
class MVGNode:
    """A node in the minimum viable graph."""

    name: str
    description: str
    is_axiom: bool = False
    concept_id: str | None = None


@dataclass
class MVGResult:
    """Result of MVG generation."""

    target: str
    domain: str
    path: list[MVGNode]
    explanation: str


_MVG_PROMPT_TEMPLATE = '''You are a knowledge graph expert. Given a target concept, identify the MINIMUM set of prerequisite concepts needed to understand it, starting from foundational axioms.

Target concept: {target}
Domain: {domain}

Rules:
1. Start from the most fundamental axioms/definitions
2. Include ONLY concepts that are DIRECTLY required to understand the target
3. Order concepts from most fundamental to the target
4. Keep the path as SHORT as possible while being complete
5. Each concept should build on previous ones

Return a JSON object with this exact structure:
{{
  "path": [
    {{"name": "concept name", "description": "brief description", "is_axiom": true/false}},
    ...
  ],
  "explanation": "Brief explanation of why this path is minimal"
}}

Return ONLY the JSON, no other text.'''


class MVGService:
    """Service for generating Minimum Viable Graphs."""

    def __init__(self):
        self._llm = get_llm_service()
        self._repo = ConceptRepository()

    async def generate(self, target: str, domain: str = "MATH") -> MVGResult:
        """Generate a minimum viable graph for a target concept.

        Args:
            target: The target concept to learn.
            domain: The knowledge domain (MATH, PHYSICS, etc.).

        Returns:
            MVGResult containing the learning path.

        Raises:
            ValueError: If the LLM response cannot be parsed.
        """
        prompt = _MVG_PROMPT_TEMPLATE.format(target=target, domain=domain)

        response = await self._llm.generate(prompt)

        # Parse JSON from response, handling potential markdown code blocks
        text = response.text.strip()
        if text.startswith("```"):
            # Remove markdown code block
            text = re.sub(r"^```(?:json)?\n?", "", text)
            text = re.sub(r"\n?```$", "", text)

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {e}")

        # Build MVGNode list, linking to existing concepts where possible
        path = []
        for item in data.get("path", []):
            concept_id = None
            # Try to find existing concept in database
            existing = self._find_concept_by_name(item["name"], domain)
            if existing:
                concept_id = existing.id

            path.append(
                MVGNode(
                    name=item["name"],
                    description=item.get("description", ""),
                    is_axiom=item.get("is_axiom", False),
                    concept_id=concept_id,
                )
            )

        return MVGResult(
            target=target,
            domain=domain,
            path=path,
            explanation=data.get("explanation", ""),
        )

    def _find_concept_by_name(self, name: str, domain: str) -> Concept | None:
        """Find a concept by name in the database."""
        # Get all concepts in domain and search by name
        # This is a simple implementation; could be optimized with a name index
        try:
            concepts = self._repo.get_by_domain(domain)
            name_lower = name.lower()
            for concept in concepts:
                if concept.name.lower() == name_lower:
                    return concept
        except Exception:
            # Database may not be available
            pass
        return None


# Module-level singleton
_mvg_service: MVGService | None = None


def get_mvg_service() -> MVGService:
    """Get the MVG service singleton."""
    global _mvg_service
    if _mvg_service is None:
        _mvg_service = MVGService()
    return _mvg_service
