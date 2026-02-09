"""Tests for DefinitionFormatter."""

import pytest

from generator.core.definition_formatter import (
    DefinitionFormatter,
    RawConceptData,
)


class MockLLMClient:
    """Mock LLM client for testing."""

    def __init__(self, response: str = "Mock formalized definition with $x^2$ notation."):
        self.response = response
        self.calls: list[str] = []

    def complete(self, prompt: str) -> str:
        self.calls.append(prompt)
        return self.response


class TestDefinitionFormatter:
    """Tests for DefinitionFormatter class."""

    def test_has_latex_inline_math(self):
        """Test detection of inline LaTeX."""
        formatter = DefinitionFormatter(llm_client=MockLLMClient())
        assert formatter._has_latex("The derivative is $f'(x)$")
        assert formatter._has_latex("For all $x \\in \\mathbb{R}$")

    def test_has_latex_display_math(self):
        """Test detection of display LaTeX."""
        formatter = DefinitionFormatter(llm_client=MockLLMClient())
        assert formatter._has_latex("The equation is $$x^2 + y^2 = r^2$$")

    def test_has_latex_environment(self):
        """Test detection of LaTeX environments."""
        formatter = DefinitionFormatter(llm_client=MockLLMClient())
        assert formatter._has_latex("\\begin{equation}x = 1\\end{equation}")

    def test_has_latex_commands(self):
        """Test detection of common LaTeX commands."""
        formatter = DefinitionFormatter(llm_client=MockLLMClient())
        assert formatter._has_latex("The sum \\sum_{i=1}^n x_i")
        assert formatter._has_latex("The integral \\int_0^1 f(x) dx")
        assert formatter._has_latex("For all \\forall x")

    def test_has_latex_negative(self):
        """Test that plain text returns False."""
        formatter = DefinitionFormatter(llm_client=MockLLMClient())
        assert not formatter._has_latex("A vector space is a set with operations")
        assert not formatter._has_latex("The derivative measures rate of change")

    def test_format_definition_with_latex(self):
        """Test formatting when definition already has LaTeX."""
        mock_llm = MockLLMClient()
        formatter = DefinitionFormatter(llm_client=mock_llm)

        raw_data = RawConceptData(
            name="Derivative",
            domain="MATH",
            definition="The **derivative** of $f$ at $a$ is $f'(a) = \\lim_{h \\to 0} \\frac{f(a+h) - f(a)}{h}$",
        )

        result = formatter.format_definition(raw_data)

        # Should NOT call LLM since definition already has LaTeX
        assert len(mock_llm.calls) == 0
        assert "## Derivative" in result
        assert "$f'(a)" in result

    def test_format_definition_without_latex(self):
        """Test that LLM is called for informal definitions."""
        mock_llm = MockLLMClient(response="A **derivative** measures the rate of change at $x$.")
        formatter = DefinitionFormatter(llm_client=mock_llm)

        raw_data = RawConceptData(
            name="Derivative",
            domain="MATH",
            definition="A derivative measures the rate of change",
        )

        result = formatter.format_definition(raw_data)

        # Should call LLM to formalize
        assert len(mock_llm.calls) == 1
        assert "Derivative" in mock_llm.calls[0]
        assert "MATH" in mock_llm.calls[0]
        assert "## Derivative" in result

    def test_format_definition_with_notations(self):
        """Test that notations are included."""
        mock_llm = MockLLMClient()
        formatter = DefinitionFormatter(llm_client=mock_llm)

        raw_data = RawConceptData(
            name="Derivative",
            domain="MATH",
            definition="$f'(a) = \\lim_{h \\to 0} \\frac{f(a+h) - f(a)}{h}$",
            notations=["f'(a)", "df/dx", "Df(a)"],
        )

        result = formatter.format_definition(raw_data)

        assert "**Notation:**" in result
        assert "`f'(a)`" in result
        assert "`df/dx`" in result
        assert "`Df(a)`" in result

    def test_format_definition_with_examples(self):
        """Test that examples are included."""
        mock_llm = MockLLMClient()
        formatter = DefinitionFormatter(llm_client=mock_llm)

        raw_data = RawConceptData(
            name="Vector Space",
            domain="MATH",
            definition="A **vector space** over $F$ is a set $V$ with addition.",
            examples=["$\\mathbb{R}^n$ is a vector space over $\\mathbb{R}$", "Polynomials form a vector space"],
        )

        result = formatter.format_definition(raw_data)

        assert "**Examples:**" in result
        assert "- $\\mathbb{R}^n$" in result
        assert "- Polynomials" in result

    def test_format_definition_from_dict(self):
        """Test that dict input is accepted."""
        mock_llm = MockLLMClient()
        formatter = DefinitionFormatter(llm_client=mock_llm)

        raw_data = {
            "name": "Empty Set",
            "domain": "MATH",
            "definition": "The set $\\emptyset$ has no elements.",
        }

        result = formatter.format_definition(raw_data)

        assert "## Empty Set" in result
        assert "$\\emptyset$" in result

    def test_format_definition_empty_definition(self):
        """Test that LLM generates definition when none provided."""
        mock_llm = MockLLMClient(response="The **Hilbert space** is a complete inner product space $H$.")
        formatter = DefinitionFormatter(llm_client=mock_llm)

        raw_data = RawConceptData(
            name="Hilbert Space",
            domain="MATH",
            definition="",
        )

        result = formatter.format_definition(raw_data)

        # Should call LLM to generate
        assert len(mock_llm.calls) == 1
        assert "Hilbert Space" in mock_llm.calls[0]
        assert "## Hilbert Space" in result

    def test_format_batch(self):
        """Test batch formatting."""
        mock_llm = MockLLMClient()
        formatter = DefinitionFormatter(llm_client=mock_llm)

        raw_data_list = [
            RawConceptData(name="Set", domain="MATH", definition="A $\\{x\\}$ collection"),
            RawConceptData(name="Function", domain="MATH", definition="A map $f: A \\to B$"),
        ]

        results = formatter.format_batch(raw_data_list)

        assert len(results) == 2
        assert "## Set" in results[0]
        assert "## Function" in results[1]
