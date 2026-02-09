"""Seed definitions for the Knowledge Tree generator.

Each domain module exports a list of seed definitions containing:
- Axioms and foundational concepts for the domain
- Formal definitions in Markdown with LaTeX notation
- Prerequisite relationships between concepts
- Reference books and papers
"""

from .mathematics import MATH_AXIOM_DEFINITIONS
from .physics import PHYSICS_AXIOM_DEFINITIONS
from .chemistry import CHEMISTRY_AXIOM_DEFINITIONS
from .biology import BIOLOGY_AXIOM_DEFINITIONS
from .computer_science import CS_AXIOM_DEFINITIONS

# Map domain names to their seed definitions
DOMAIN_SEEDS = {
    "MATH": MATH_AXIOM_DEFINITIONS,
    "PHYSICS": PHYSICS_AXIOM_DEFINITIONS,
    "CHEMISTRY": CHEMISTRY_AXIOM_DEFINITIONS,
    "BIOLOGY": BIOLOGY_AXIOM_DEFINITIONS,
    "CS": CS_AXIOM_DEFINITIONS,
}

__all__ = [
    "MATH_AXIOM_DEFINITIONS",
    "PHYSICS_AXIOM_DEFINITIONS",
    "CHEMISTRY_AXIOM_DEFINITIONS",
    "BIOLOGY_AXIOM_DEFINITIONS",
    "CS_AXIOM_DEFINITIONS",
    "DOMAIN_SEEDS",
]
