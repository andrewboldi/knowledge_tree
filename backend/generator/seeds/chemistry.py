"""Chemistry seed definitions - fundamental laws and concepts."""

CHEMISTRY_AXIOM_DEFINITIONS = [
    {
        "name": "Law of Conservation of Mass",
        "definition_md": """## Law of Conservation of Mass

In a closed system, mass is neither created nor destroyed in chemical reactions:

$$\\sum m_{reactants} = \\sum m_{products}$$

**Implication:** Atoms are rearranged, not created or destroyed.""",
        "domain": "CHEMISTRY",
        "subfield": "general",
        "complexity_level": 0,
        "is_axiom": True,
        "books": ["Chemistry - Zumdahl", "General Chemistry - Petrucci"],
        "prerequisites": []
    },
    {
        "name": "Law of Definite Proportions",
        "definition_md": """## Law of Definite Proportions (Proust's Law)

A chemical compound always contains the same elements in the same
proportion by mass, regardless of source or method of preparation.

**Example:** Water ($H_2O$) always contains hydrogen and oxygen
in a mass ratio of 1:8.""",
        "domain": "CHEMISTRY",
        "subfield": "general",
        "complexity_level": 0,
        "is_axiom": True,
        "books": ["Chemistry - Zumdahl"],
        "prerequisites": []
    },
    {
        "name": "First Law of Thermodynamics",
        "definition_md": """## First Law of Thermodynamics

Energy cannot be created or destroyed, only transferred or converted:

$$\\Delta U = q + w$$

where:
- $\\Delta U$ is change in internal energy
- $q$ is heat added to the system
- $w$ is work done on the system""",
        "domain": "CHEMISTRY",
        "subfield": "thermodynamics",
        "complexity_level": 0,
        "is_axiom": True,
        "books": ["Physical Chemistry - Atkins", "Chemical Thermodynamics - Denbigh"],
        "prerequisites": []
    },
]
