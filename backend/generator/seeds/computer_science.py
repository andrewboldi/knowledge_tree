"""Computer Science seed definitions - foundational concepts."""

CS_AXIOM_DEFINITIONS = [
    {
        "name": "Turing Machine",
        "definition_md": """## Turing Machine

A **Turing machine** is a mathematical model of computation consisting of:

1. An infinite tape divided into cells, each containing a symbol
2. A head that reads/writes symbols and moves left/right
3. A state register storing the current state
4. A finite table of instructions (transition function)

$$\\delta: Q \\times \\Gamma \\to Q \\times \\Gamma \\times \\{L, R\\}$$

where $Q$ is the set of states and $\\Gamma$ is the tape alphabet.""",
        "domain": "CS",
        "subfield": "theory_of_computation",
        "complexity_level": 0,
        "is_axiom": True,
        "books": ["Introduction to the Theory of Computation - Sipser", "Computability and Logic - Boolos"],
        "prerequisites": []
    },
    {
        "name": "Church-Turing Thesis",
        "definition_md": """## Church-Turing Thesis

A function on the natural numbers is **computable** if and only if it is
computable by a Turing machine.

**Equivalently:** All reasonable models of computation are equivalent in power.

This is a **thesis** (philosophical claim), not a theorem, as "computable"
is an informal notion.""",
        "domain": "CS",
        "subfield": "theory_of_computation",
        "complexity_level": 0,
        "is_axiom": True,
        "books": ["Introduction to the Theory of Computation - Sipser"],
        "prerequisites": ["Turing Machine"]
    },
    {
        "name": "Big-O Notation",
        "definition_md": """## Big-O Notation

A function $f(n)$ is $O(g(n))$ if there exist positive constants $c$ and $n_0$ such that:

$$0 \\leq f(n) \\leq c \\cdot g(n) \\quad \\forall n \\geq n_0$$

**Interpretation:** $f$ grows no faster than $g$ asymptotically.

**Common classes:**
- $O(1)$ - constant
- $O(\\log n)$ - logarithmic
- $O(n)$ - linear
- $O(n \\log n)$ - linearithmic
- $O(n^2)$ - quadratic
- $O(2^n)$ - exponential""",
        "domain": "CS",
        "subfield": "algorithms",
        "complexity_level": 1,
        "is_axiom": False,
        "books": ["Introduction to Algorithms - CLRS", "Algorithm Design - Kleinberg & Tardos"],
        "prerequisites": []
    },
]
