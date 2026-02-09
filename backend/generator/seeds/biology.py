"""Biology seed definitions - central dogma and fundamental principles."""

BIOLOGY_AXIOM_DEFINITIONS = [
    {
        "name": "Central Dogma of Molecular Biology",
        "definition_md": """## Central Dogma of Molecular Biology

Genetic information flows from DNA to RNA to protein:

$$\\text{DNA} \\xrightarrow{\\text{transcription}} \\text{RNA} \\xrightarrow{\\text{translation}} \\text{Protein}$$

**Exceptions:**
- Reverse transcription (RNA → DNA) in retroviruses
- RNA replication in some viruses""",
        "domain": "BIOLOGY",
        "subfield": "molecular_biology",
        "complexity_level": 0,
        "is_axiom": True,
        "books": ["Molecular Biology of the Cell - Alberts", "Molecular Biology of the Gene - Watson"],
        "prerequisites": []
    },
    {
        "name": "Cell Theory",
        "definition_md": """## Cell Theory

The fundamental principles of cell biology:

1. All living organisms are composed of one or more cells
2. The cell is the basic unit of structure and function in organisms
3. All cells arise from pre-existing cells

$$\\text{omnis cellula e cellula}$$
("every cell from a cell" - Virchow)""",
        "domain": "BIOLOGY",
        "subfield": "cell_biology",
        "complexity_level": 0,
        "is_axiom": True,
        "books": ["Biology - Campbell", "Molecular Biology of the Cell - Alberts"],
        "prerequisites": []
    },
    {
        "name": "Natural Selection",
        "definition_md": """## Natural Selection

The differential survival and reproduction of individuals due to differences
in phenotype, leading to evolutionary change:

**Requirements:**
1. **Variation:** Individuals differ in traits
2. **Inheritance:** Traits are heritable
3. **Selection:** Some traits improve survival/reproduction
4. **Time:** Sufficient generations for change

$$\\Delta p = p(1-p) \\cdot s$$

where $p$ is allele frequency and $s$ is selection coefficient.""",
        "domain": "BIOLOGY",
        "subfield": "evolution",
        "complexity_level": 0,
        "is_axiom": True,
        "books": ["On the Origin of Species - Darwin", "Evolutionary Biology - Futuyma"],
        "prerequisites": []
    },
]
