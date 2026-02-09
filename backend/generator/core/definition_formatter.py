"""Definition formatter for converting raw concepts to formal Markdown + LaTeX."""

import os
import re
from dataclasses import dataclass
from typing import Protocol

import httpx


class LLMClient(Protocol):
    """Protocol for LLM clients."""

    def complete(self, prompt: str) -> str:
        """Generate a completion for the given prompt."""
        ...


@dataclass
class RawConceptData:
    """Raw concept data extracted from sources."""

    name: str
    domain: str
    definition: str = ""
    subfield: str = ""
    notations: list[str] | None = None
    examples: list[str] | None = None


class OpenAICompatibleClient:
    """Client for OpenAI-compatible LLM APIs (Kimi K2.5, OpenAI, etc.)."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
    ):
        self.api_key = api_key or os.getenv("LLM_API_KEY", "")
        self.base_url = base_url or os.getenv(
            "LLM_BASE_URL", "https://api.openai.com/v1"
        )
        self.model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")
        self._client = httpx.Client(timeout=60.0)

    def complete(self, prompt: str) -> str:
        """Generate a completion using the LLM API."""
        response = self._client.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a precise mathematical definition formatter. "
                            "Convert informal definitions into rigorous formal definitions "
                            "with proper LaTeX notation. Be concise and accurate."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.3,
                "max_tokens": 1024,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


class DefinitionFormatter:
    """Convert extracted concept info into formal Markdown + LaTeX definition."""

    # Patterns to detect LaTeX in text
    LATEX_PATTERNS = [
        r"\$[^$]+\$",  # Inline math: $...$
        r"\$\$[^$]+\$\$",  # Display math: $$...$$
        r"\\begin\{[^}]+\}",  # LaTeX environments
        r"\\frac\{",  # Common LaTeX commands
        r"\\sum",
        r"\\int",
        r"\\lim",
        r"\\mathbb\{",
        r"\\forall",
        r"\\exists",
        r"\\in",
        r"\\subseteq",
    ]

    def __init__(self, llm_client: LLMClient | None = None):
        """Initialize formatter with optional LLM client.

        Args:
            llm_client: LLM client for formalizing definitions.
                       If None, uses OpenAICompatibleClient with env vars.
        """
        self._llm = llm_client or OpenAICompatibleClient()

    def format_definition(self, raw_data: RawConceptData | dict) -> str:
        """Generate a formal definition card in Markdown with LaTeX.

        Uses LLM to enhance/formalize if raw definition is informal.

        Args:
            raw_data: Raw concept data (RawConceptData or dict with same fields)

        Returns:
            Formatted Markdown definition with LaTeX
        """
        if isinstance(raw_data, dict):
            raw_data = RawConceptData(**raw_data)

        name = raw_data.name
        raw_def = raw_data.definition
        domain = raw_data.domain

        # If definition lacks LaTeX, use LLM to formalize
        if raw_def and not self._has_latex(raw_def):
            formal_def = self._formalize_with_llm(name, raw_def, domain)
        else:
            formal_def = raw_def or self._generate_definition_with_llm(name, domain)

        # Structure the definition
        md = f"## {name}\n\n{formal_def}"

        # Add notation section if applicable
        if raw_data.notations:
            notations_str = ", ".join(f"`{n}`" for n in raw_data.notations)
            md += f"\n\n**Notation:** {notations_str}"

        # Add examples if available
        if raw_data.examples:
            md += "\n\n**Examples:**\n"
            for ex in raw_data.examples:
                md += f"- {ex}\n"

        return md

    def _has_latex(self, text: str) -> bool:
        """Check if text contains LaTeX notation."""
        for pattern in self.LATEX_PATTERNS:
            if re.search(pattern, text):
                return True
        return False

    def _formalize_with_llm(self, name: str, informal_def: str, domain: str) -> str:
        """Use LLM to add proper LaTeX notation to informal definition."""
        prompt = f"""Convert this informal definition into a formal mathematical definition
with proper LaTeX notation. Use $...$ for inline math and $$...$$ for display math.

Term: {name}
Domain: {domain}
Informal definition: {informal_def}

Return ONLY the formal definition in Markdown with LaTeX. Be precise and rigorous.
Do not include the term name as a header - just the definition body."""

        return self._llm.complete(prompt)

    def _generate_definition_with_llm(self, name: str, domain: str) -> str:
        """Generate a complete definition using LLM when no definition exists."""
        prompt = f"""Write a formal mathematical definition for the following term.
Use proper LaTeX notation with $...$ for inline math and $$...$$ for display math.

Term: {name}
Domain: {domain}

Return ONLY the formal definition in Markdown with LaTeX. Be precise and rigorous.
Include the key properties and any standard notation.
Do not include the term name as a header - just the definition body."""

        return self._llm.complete(prompt)

    def format_batch(self, raw_data_list: list[RawConceptData | dict]) -> list[str]:
        """Format multiple concept definitions.

        Args:
            raw_data_list: List of raw concept data

        Returns:
            List of formatted Markdown definitions
        """
        return [self.format_definition(data) for data in raw_data_list]
