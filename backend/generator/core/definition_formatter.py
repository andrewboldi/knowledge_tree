"""Definition formatter - converts extracted info to formal Markdown + LaTeX."""

import re


class DefinitionFormatter:
    """Convert extracted concept info into formal Markdown + LaTeX definition."""

    def format_definition(self, raw_data: dict) -> str:
        """
        Generate a formal definition card in Markdown with LaTeX.

        Uses LLM to enhance/formalize if raw definition is informal.
        """
        name = raw_data["name"]
        raw_def = raw_data.get("definition", "")
        domain = raw_data["domain"]

        if not self._has_latex(raw_def):
            formal_def = self._formalize_with_llm(name, raw_def, domain)
        else:
            formal_def = raw_def

        md = f"## {name}\n\n{formal_def}"

        if notations := raw_data.get("notations"):
            md += f"\n\n**Notation:** {', '.join(notations)}"

        if examples := raw_data.get("examples"):
            md += "\n\n**Examples:**\n"
            for ex in examples:
                md += f"- {ex}\n"

        return md

    def _has_latex(self, text: str) -> bool:
        """Check if text contains LaTeX notation."""
        return bool(re.search(r'\$.*?\$|\\\[.*?\\\]', text))

    def _formalize_with_llm(self, name: str, informal_def: str, domain: str) -> str:
        """Use LLM to add proper LaTeX notation to informal definition."""
        raise NotImplementedError("LLM formalization not yet implemented")
