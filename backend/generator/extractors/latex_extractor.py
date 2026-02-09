"""LaTeX notation extractor and generator."""

import re

from .base import BaseExtractor, ExtractedConcept


class LatexExtractor(BaseExtractor):
    """Extract and generate LaTeX notation for mathematical concepts.

    This extractor identifies mathematical notation in text and converts
    it to proper LaTeX format, or generates LaTeX notation based on
    known patterns for common mathematical objects.
    """

    # Common mathematical symbols and their LaTeX equivalents
    SYMBOL_MAP = {
        # Greek letters
        "alpha": r"\alpha",
        "beta": r"\beta",
        "gamma": r"\gamma",
        "delta": r"\delta",
        "epsilon": r"\epsilon",
        "zeta": r"\zeta",
        "eta": r"\eta",
        "theta": r"\theta",
        "iota": r"\iota",
        "kappa": r"\kappa",
        "lambda": r"\lambda",
        "mu": r"\mu",
        "nu": r"\nu",
        "xi": r"\xi",
        "pi": r"\pi",
        "rho": r"\rho",
        "sigma": r"\sigma",
        "tau": r"\tau",
        "upsilon": r"\upsilon",
        "phi": r"\phi",
        "chi": r"\chi",
        "psi": r"\psi",
        "omega": r"\omega",
        # Uppercase Greek
        "Gamma": r"\Gamma",
        "Delta": r"\Delta",
        "Theta": r"\Theta",
        "Lambda": r"\Lambda",
        "Xi": r"\Xi",
        "Pi": r"\Pi",
        "Sigma": r"\Sigma",
        "Phi": r"\Phi",
        "Psi": r"\Psi",
        "Omega": r"\Omega",
        # Common mathematical symbols
        "infinity": r"\infty",
        "partial": r"\partial",
        "nabla": r"\nabla",
        "forall": r"\forall",
        "exists": r"\exists",
        "emptyset": r"\emptyset",
        "in": r"\in",
        "notin": r"\notin",
        "subset": r"\subset",
        "supset": r"\supset",
        "cup": r"\cup",
        "cap": r"\cap",
        "implies": r"\implies",
        "iff": r"\iff",
        "mapsto": r"\mapsto",
        "rightarrow": r"\rightarrow",
        "leftarrow": r"\leftarrow",
        "leftrightarrow": r"\leftrightarrow",
        "sum": r"\sum",
        "prod": r"\prod",
        "int": r"\int",
        "sqrt": r"\sqrt",
        # Number sets
        "naturals": r"\mathbb{N}",
        "integers": r"\mathbb{Z}",
        "rationals": r"\mathbb{Q}",
        "reals": r"\mathbb{R}",
        "complex": r"\mathbb{C}",
    }

    # Patterns for common mathematical expressions
    NOTATION_PATTERNS: dict[str, dict[str, str]] = {
        # Functions
        "function": {
            "pattern": r"f\s*:\s*([A-Z])\s*(?:->|→|to)\s*([A-Z])",
            "latex": r"f: {domain} \to {codomain}",
        },
        # Sets
        "set_builder": {
            "pattern": r"\{\s*x\s*[:|]\s*([^}]+)\}",
            "latex": r"\{x \mid {condition}\}",
        },
        # Derivatives
        "derivative": {
            "pattern": r"d([a-z])/d([a-z])",
            "latex": r"\frac{d{var1}}{d{var2}}",
        },
        # Partial derivatives
        "partial_derivative": {
            "pattern": r"∂([a-z])/∂([a-z])",
            "latex": r"\frac{\partial {var1}}{\partial {var2}}",
        },
        # Limits
        "limit": {
            "pattern": r"lim(?:it)?\s*(?:as\s*)?([a-z])\s*(?:->|→|approaches?)\s*([a-z0-9∞]+)",
            "latex": r"\lim_{{var} \to {target}}",
        },
        # Integrals
        "integral": {
            "pattern": r"∫\s*([^d]+)\s*d([a-z])",
            "latex": r"\int {integrand} \, d{var}",
        },
        # Summation
        "summation": {
            "pattern": r"Σ|sum\s*(?:from|over)\s*([a-z])\s*=\s*(\d+)\s*to\s*([a-z0-9∞]+)",
            "latex": r"\sum_{{var}={start}}^{{end}}",
        },
    }

    # Domain-specific notation templates
    DOMAIN_TEMPLATES: dict[str, dict[str, str]] = {
        "MATH": {
            "vector_space": r"A **vector space** over a field $F$ is a set $V$ with operations $+: V \times V \to V$ and $\cdot: F \times V \to V$",
            "group": r"A **group** $(G, *)$ is a set $G$ with a binary operation $*: G \times G \to G$",
            "ring": r"A **ring** $(R, +, \cdot)$ is a set with two binary operations satisfying ring axioms",
            "field": r"A **field** $(F, +, \cdot)$ is a commutative ring where every nonzero element has a multiplicative inverse",
            "topology": r"A **topology** on a set $X$ is a collection $\mathcal{T} \subseteq \mathcal{P}(X)$",
            "metric_space": r"A **metric space** $(X, d)$ is a set $X$ with a function $d: X \times X \to \mathbb{R}$",
        },
        "PHYSICS": {
            "force": r"$\mathbf{F} = m\mathbf{a}$",
            "energy": r"$E = mc^2$ or $E = \frac{1}{2}mv^2 + V(x)$",
            "wave_equation": r"$\nabla^2 \psi - \frac{1}{c^2}\frac{\partial^2 \psi}{\partial t^2} = 0$",
            "schrodinger": r"$i\hbar\frac{\partial}{\partial t}\Psi = \hat{H}\Psi$",
        },
        "CHEMISTRY": {
            "rate_law": r"$r = k[A]^m[B]^n$",
            "ideal_gas": r"$PV = nRT$",
            "gibbs_free_energy": r"$\Delta G = \Delta H - T\Delta S$",
        },
    }

    def extract(self, term: str, domain: str, subfield: str) -> ExtractedConcept | None:
        """Extract/generate LaTeX notation for a term.

        This extractor doesn't fetch from external sources but generates
        LaTeX based on known patterns and templates.
        """
        latex_fragments = []
        notations = []

        # Check if we have a domain template
        domain_templates = self.DOMAIN_TEMPLATES.get(domain.upper(), {})
        term_lower = term.lower().replace(" ", "_")

        for template_name, template in domain_templates.items():
            if template_name in term_lower or term_lower in template_name:
                latex_fragments.append(template)
                break

        # Generate notation suggestions based on term name
        notation_suggestions = self._suggest_notation(term, domain)
        notations.extend(notation_suggestions)

        if not latex_fragments and not notations:
            return None

        return ExtractedConcept(
            name=term,
            raw_definition="",  # LaTeX extractor focuses on notation
            domain=domain,
            subfield=subfield,
            source_type="latex_generator",
            latex_fragments=latex_fragments,
            notations=notations,
        )

    def can_extract(self, term: str) -> bool:
        """LaTeX extractor can always attempt to generate notation."""
        return True

    def extract_latex_from_text(self, text: str) -> list[str]:
        """Extract existing LaTeX notation from text.

        Finds both inline ($...$) and display ($$...$$) math.
        """
        fragments = []

        # Display math: $$...$$
        display_pattern = re.compile(r"\$\$([^$]+)\$\$")
        for match in display_pattern.finditer(text):
            fragments.append(match.group(1).strip())

        # Inline math: $...$  (not greedy, avoid $$)
        inline_pattern = re.compile(r"(?<!\$)\$([^$]+)\$(?!\$)")
        for match in inline_pattern.finditer(text):
            fragments.append(match.group(1).strip())

        return fragments

    def convert_unicode_to_latex(self, text: str) -> str:
        """Convert Unicode mathematical symbols to LaTeX."""
        replacements = {
            "→": r"\to",
            "←": r"\leftarrow",
            "↔": r"\leftrightarrow",
            "⇒": r"\Rightarrow",
            "⇐": r"\Leftarrow",
            "⇔": r"\Leftrightarrow",
            "∀": r"\forall",
            "∃": r"\exists",
            "∈": r"\in",
            "∉": r"\notin",
            "⊂": r"\subset",
            "⊃": r"\supset",
            "⊆": r"\subseteq",
            "⊇": r"\supseteq",
            "∪": r"\cup",
            "∩": r"\cap",
            "∅": r"\emptyset",
            "∞": r"\infty",
            "∂": r"\partial",
            "∇": r"\nabla",
            "∑": r"\sum",
            "∏": r"\prod",
            "∫": r"\int",
            "≤": r"\leq",
            "≥": r"\geq",
            "≠": r"\neq",
            "≈": r"\approx",
            "≡": r"\equiv",
            "±": r"\pm",
            "×": r"\times",
            "÷": r"\div",
            "·": r"\cdot",
            "√": r"\sqrt",
            "ℕ": r"\mathbb{N}",
            "ℤ": r"\mathbb{Z}",
            "ℚ": r"\mathbb{Q}",
            "ℝ": r"\mathbb{R}",
            "ℂ": r"\mathbb{C}",
            # Greek letters
            "α": r"\alpha",
            "β": r"\beta",
            "γ": r"\gamma",
            "δ": r"\delta",
            "ε": r"\epsilon",
            "ζ": r"\zeta",
            "η": r"\eta",
            "θ": r"\theta",
            "ι": r"\iota",
            "κ": r"\kappa",
            "λ": r"\lambda",
            "μ": r"\mu",
            "ν": r"\nu",
            "ξ": r"\xi",
            "π": r"\pi",
            "ρ": r"\rho",
            "σ": r"\sigma",
            "τ": r"\tau",
            "υ": r"\upsilon",
            "φ": r"\phi",
            "χ": r"\chi",
            "ψ": r"\psi",
            "ω": r"\omega",
            "Γ": r"\Gamma",
            "Δ": r"\Delta",
            "Θ": r"\Theta",
            "Λ": r"\Lambda",
            "Ξ": r"\Xi",
            "Π": r"\Pi",
            "Σ": r"\Sigma",
            "Φ": r"\Phi",
            "Ψ": r"\Psi",
            "Ω": r"\Omega",
        }

        result = text
        for unicode_char, latex in replacements.items():
            result = result.replace(unicode_char, latex)

        return result

    def _suggest_notation(self, term: str, domain: str) -> list[str]:
        """Suggest common notation for a term based on its name."""
        suggestions = []
        term_lower = term.lower()

        # Common mathematical object notations
        if "function" in term_lower:
            suggestions.append("f, g, h")
            suggestions.append("f: X → Y")

        if "set" in term_lower:
            suggestions.append("A, B, C (sets)")
            suggestions.append("{x | condition}")

        if "vector" in term_lower:
            suggestions.append("v, u, w (bold or arrow)")
            suggestions.append("⟨v, w⟩ (inner product)")

        if "matrix" in term_lower:
            suggestions.append("A, B, M (capital letters)")
            suggestions.append("aᵢⱼ (entries)")

        if "limit" in term_lower:
            suggestions.append("lim_{x→a}")

        if "derivative" in term_lower:
            suggestions.append("f'(x), df/dx, Df")

        if "integral" in term_lower:
            suggestions.append("∫ f(x) dx")

        if "sum" in term_lower:
            suggestions.append("Σ_{i=1}^n")

        if "product" in term_lower:
            suggestions.append("∏_{i=1}^n")

        return suggestions

    def enrich_with_latex(self, concept: ExtractedConcept) -> ExtractedConcept:
        """Enrich an existing concept with LaTeX notation.

        Analyzes the raw_definition and adds LaTeX fragments.
        """
        # Extract any existing LaTeX from the definition
        existing = self.extract_latex_from_text(concept.raw_definition)
        concept.latex_fragments.extend(existing)

        # Convert any Unicode math symbols
        concept.raw_definition = self.convert_unicode_to_latex(concept.raw_definition)

        # Add notation suggestions
        suggestions = self._suggest_notation(concept.name, concept.domain)
        concept.notations.extend(s for s in suggestions if s not in concept.notations)

        return concept
