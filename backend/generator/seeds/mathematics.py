"""Mathematics seed definitions - ZFC axioms with formal definitions."""

MATH_AXIOM_DEFINITIONS = [
    {
        "name": "Axiom of Extensionality",
        "definition_md": """## Axiom of Extensionality

Two sets are equal if and only if they contain the same elements:

$$\\forall A \\forall B \\left( \\forall x (x \\in A \\iff x \\in B) \\implies A = B \\right)$$

**Informal:** Sets are determined entirely by their members.""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": ["Set Theory - Kunen, Ch. 1", "Naive Set Theory - Halmos"],
        "prerequisites": []
    },
    {
        "name": "Empty Set",
        "definition_md": """## Empty Set

The **empty set** (or null set), denoted $\\emptyset$ or $\\{\\}$, is the unique set with no elements:

$$\\forall x (x \\notin \\emptyset)$$

**Existence (Axiom of Empty Set):**
$$\\exists A \\forall x (x \\notin A)$$

**Uniqueness:** By extensionality, there is exactly one empty set.""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": ["Set Theory - Kunen, Ch. 1"],
        "prerequisites": ["Axiom of Extensionality"]
    },
    {
        "name": "Axiom of Pairing",
        "definition_md": """## Axiom of Pairing

For any two sets $a$ and $b$, there exists a set containing exactly $a$ and $b$:

$$\\forall a \\forall b \\exists c \\forall x (x \\in c \\iff x = a \\lor x = b)$$

This set is denoted $\\{a, b\\}$.""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": ["Set Theory - Kunen, Ch. 1"],
        "prerequisites": []
    },
    {
        "name": "Ordered Pair",
        "definition_md": """## Ordered Pair

The **ordered pair** $(a, b)$ is defined (Kuratowski definition) as:

$$(a, b) := \\{\\{a\\}, \\{a, b\\}\\}$$

**Characteristic property:**
$$(a, b) = (c, d) \\iff a = c \\land b = d$$

This distinguishes ordered pairs from unordered pairs $\\{a, b\\}$ where order doesn't matter.""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 1,
        "is_axiom": False,
        "books": ["Set Theory - Kunen, Ch. 1"],
        "prerequisites": ["Axiom of Pairing"]
    },
]
