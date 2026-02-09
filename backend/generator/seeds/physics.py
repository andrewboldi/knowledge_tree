"""Physics seed definitions - fundamental laws and axioms."""

PHYSICS_AXIOM_DEFINITIONS = [
    {
        "name": "Newton's First Law",
        "definition_md": """## Newton's First Law (Law of Inertia)

A body remains at rest, or in motion at a constant speed in a straight line,
unless acted upon by a net external force:

$$\\mathbf{F}_{net} = 0 \\implies \\frac{d\\mathbf{v}}{dt} = 0$$

**Inertial reference frame:** A frame where this law holds.""",
        "domain": "PHYSICS",
        "subfield": "mechanics",
        "complexity_level": 0,
        "is_axiom": True,
        "books": ["Principia Mathematica - Newton", "Classical Mechanics - Goldstein"],
        "prerequisites": []
    },
    {
        "name": "Newton's Second Law",
        "definition_md": """## Newton's Second Law

The rate of change of momentum of a body equals the net force acting on it:

$$\\mathbf{F} = \\frac{d\\mathbf{p}}{dt} = \\frac{d(m\\mathbf{v})}{dt}$$

For constant mass:

$$\\mathbf{F} = m\\mathbf{a}$$

where:
- $\\mathbf{F}$ is the net force (N)
- $m$ is mass (kg)
- $\\mathbf{a}$ is acceleration (m/s²)""",
        "domain": "PHYSICS",
        "subfield": "mechanics",
        "complexity_level": 0,
        "is_axiom": True,
        "books": ["Principia Mathematica - Newton", "Classical Mechanics - Goldstein"],
        "prerequisites": []
    },
    {
        "name": "Conservation of Energy",
        "definition_md": """## Conservation of Energy

In an isolated system, the total energy remains constant over time:

$$\\frac{dE_{total}}{dt} = 0$$

Or equivalently:

$$E_{total} = K + U = \\text{constant}$$

where $K$ is kinetic energy and $U$ is potential energy.""",
        "domain": "PHYSICS",
        "subfield": "mechanics",
        "complexity_level": 0,
        "is_axiom": True,
        "books": ["Classical Mechanics - Goldstein", "Feynman Lectures on Physics"],
        "prerequisites": []
    },
]
