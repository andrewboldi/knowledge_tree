"""LLM service using opencode CLI with Kimi K2.5."""

import asyncio
import json
import os
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Response from LLM."""

    text: str
    input_tokens: int
    output_tokens: int


class LLMService:
    """Service for interacting with LLMs via opencode CLI."""

    def __init__(self, model: str = "opencode/kimi-k2.5"):
        self.model = model
        self._opencode_path = os.environ.get(
            "OPENCODE_PATH", os.path.expanduser("~/.opencode/bin/opencode")
        )

    async def generate(self, prompt: str) -> LLMResponse:
        """Generate a response from the LLM.

        Args:
            prompt: The prompt to send to the LLM.

        Returns:
            LLMResponse containing the generated text and token counts.

        Raises:
            RuntimeError: If opencode fails or returns no text.
        """
        process = await asyncio.create_subprocess_exec(
            self._opencode_path,
            "run",
            "-m",
            self.model,
            "--format",
            "json",
            prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"opencode failed: {stderr.decode()}")

        # Parse JSON events from stdout
        text_parts = []
        input_tokens = 0
        output_tokens = 0

        for line in stdout.decode().strip().split("\n"):
            if not line:
                continue
            try:
                event = json.loads(line)
                if event.get("type") == "text":
                    text_parts.append(event["part"]["text"])
                elif event.get("type") == "step_finish":
                    tokens = event.get("part", {}).get("tokens", {})
                    input_tokens = tokens.get("input", 0)
                    output_tokens = tokens.get("output", 0)
            except json.JSONDecodeError:
                continue

        if not text_parts:
            raise RuntimeError("No text response from LLM")

        return LLMResponse(
            text="".join(text_parts),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )


# Module-level singleton
_llm_service: LLMService | None = None


def get_llm_service() -> LLMService:
    """Get the LLM service singleton."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
