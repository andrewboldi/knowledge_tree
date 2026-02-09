"""Biology seed definitions - fundamental concepts of life sciences.

This module contains formal definitions of foundational biology concepts,
from cell theory to genetics and molecular biology.
Each definition includes:
- name: The canonical name of the concept
- definition_md: Formal definition in Markdown with LaTeX notation
- domain: Always "BIOLOGY" for this module
- subfield: The biology subfield (e.g., "cell_biology", "genetics", "molecular")
- complexity_level: 0 for fundamental principles, higher for derived concepts
- is_axiom: True for fundamental postulates/theories
- books: Reference texts where the concept is covered
- prerequisites: List of concept names that must be understood first
"""

BIOLOGY_AXIOM_DEFINITIONS = [
    # ==========================================================================
    # CELL THEORY - Level 0 (Foundational)
    # ==========================================================================
    {
        "name": "Cell Theory",
        "definition_md": """## Cell Theory

The **cell theory** is a fundamental principle of biology:

1. **All living organisms are composed of cells**
   - Cells are the basic structural unit of life
   - Unicellular organisms consist of one cell
   - Multicellular organisms consist of many specialized cells

2. **The cell is the basic unit of life**
   - Cells are the smallest units that perform all life functions
   - All metabolic processes occur within cells

3. **All cells arise from pre-existing cells**
   - *Omnis cellula e cellula* (Rudolf Virchow, 1855)
   - Cells divide to produce new cells
   - Spontaneous generation does not occur

**Modern additions:**
- Cells contain hereditary information (DNA)
- All cells have the same basic chemical composition
- Energy flow occurs within cells through ATP

**Cell types:**
- **Prokaryotic:** No membrane-bound nucleus (bacteria, archaea)
- **Eukaryotic:** Membrane-bound nucleus (animals, plants, fungi, protists)""",
        "domain": "BIOLOGY",
        "subfield": "cell_biology",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Molecular Biology of the Cell - Alberts et al., Ch. 1",
            "Campbell Biology - Ch. 6",
            "The Cell - Cooper, Ch. 1",
        ],
        "prerequisites": [],
    },
    {
        "name": "Cell",
        "definition_md": """## Cell

A **cell** is the structural and functional unit of all living organisms:

**Universal features:**
- **Plasma membrane:** Phospholipid bilayer enclosing the cell
- **Cytoplasm:** Aqueous interior containing organelles
- **Genetic material:** DNA encoding hereditary information
- **Ribosomes:** Sites of protein synthesis

**Prokaryotic cells** (bacteria, archaea):
- No membrane-bound nucleus; DNA in nucleoid region
- No membrane-bound organelles
- Size: typically $1$-$10$ $\\mu$m
- Cell wall (peptidoglycan in bacteria)

**Eukaryotic cells** (animals, plants, fungi):
- Membrane-bound nucleus containing DNA
- Membrane-bound organelles (mitochondria, ER, Golgi)
- Size: typically $10$-$100$ $\\mu$m
- Complex internal cytoskeleton

**Cell size limits:**
- Minimum: Must contain sufficient molecules for metabolism
- Maximum: Limited by surface area to volume ratio
$$\\frac{SA}{V} = \\frac{4\\pi r^2}{\\frac{4}{3}\\pi r^3} = \\frac{3}{r}$$""",
        "domain": "BIOLOGY",
        "subfield": "cell_biology",
        "complexity_level": 0,
        "is_axiom": False,
        "books": [
            "Molecular Biology of the Cell - Alberts et al., Ch. 1",
            "Campbell Biology - Ch. 6",
        ],
        "prerequisites": ["Cell Theory"],
    },
    # ==========================================================================
    # CENTRAL DOGMA - Level 0 (Foundational)
    # ==========================================================================
    {
        "name": "Central Dogma of Molecular Biology",
        "definition_md": """## Central Dogma of Molecular Biology

The **central dogma** describes the flow of genetic information:

$$\\text{DNA} \\xrightarrow{\\text{replication}} \\text{DNA}$$
$$\\text{DNA} \\xrightarrow{\\text{transcription}} \\text{RNA} \\xrightarrow{\\text{translation}} \\text{Protein}$$

**Key processes:**

1. **Replication:** DNA $\\to$ DNA
   - DNA polymerase synthesizes new DNA strand
   - Semi-conservative: each new molecule has one old, one new strand

2. **Transcription:** DNA $\\to$ RNA
   - RNA polymerase synthesizes mRNA from DNA template
   - Occurs in nucleus (eukaryotes)

3. **Translation:** RNA $\\to$ Protein
   - Ribosomes read mRNA codons
   - tRNA brings amino acids
   - Occurs in cytoplasm

**Exceptions:**
- **Reverse transcription:** RNA $\\to$ DNA (retroviruses)
- **RNA replication:** RNA $\\to$ RNA (some viruses)

**Note:** Information flows DNA $\\to$ RNA $\\to$ Protein, but NOT
Protein $\\to$ RNA $\\to$ DNA (no "reverse translation").""",
        "domain": "BIOLOGY",
        "subfield": "molecular",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Molecular Biology of the Cell - Alberts et al., Ch. 6",
            "Molecular Biology of the Gene - Watson et al., Ch. 2",
            "Genes XII - Lewin, Ch. 1",
        ],
        "prerequisites": ["Cell Theory"],
    },
    {
        "name": "DNA",
        "definition_md": """## DNA (Deoxyribonucleic Acid)

**DNA** is the molecule that carries genetic information:

**Structure (Watson-Crick model, 1953):**
- Double helix with antiparallel strands
- Sugar-phosphate backbone (deoxyribose + phosphate)
- Nitrogenous bases pair via hydrogen bonds

**Base pairing rules:**
$$\\text{A} \\equiv \\text{T} \\quad (2 \\text{ H-bonds})$$
$$\\text{G} \\equiv \\text{C} \\quad (3 \\text{ H-bonds})$$

**Chargaff's rules:**
$$[\\text{A}] = [\\text{T}], \\quad [\\text{G}] = [\\text{C}]$$

**Dimensions:**
- Helix diameter: 2 nm
- Base pair spacing: 0.34 nm
- One turn: 10.5 bp, 3.4 nm

**Directionality:**
- 5' end: free phosphate group
- 3' end: free hydroxyl group
- Strands run 5' $\\to$ 3' antiparallel

**Forms:**
- B-DNA: Right-handed, most common
- A-DNA: Right-handed, dehydrated
- Z-DNA: Left-handed, GC-rich sequences""",
        "domain": "BIOLOGY",
        "subfield": "molecular",
        "complexity_level": 0,
        "is_axiom": False,
        "books": [
            "Molecular Biology of the Cell - Alberts et al., Ch. 4",
            "Molecular Biology of the Gene - Watson et al., Ch. 4",
        ],
        "prerequisites": ["Central Dogma of Molecular Biology"],
    },
    {
        "name": "Gene",
        "definition_md": """## Gene

A **gene** is a unit of heredity; a segment of DNA that encodes a functional product:

**Classical definition:** A heritable factor that determines a phenotype.

**Molecular definition:** A DNA sequence that is transcribed into RNA.

**Gene structure (eukaryotes):**
```
5'—[Promoter]—[5'UTR]—[Exon1]—[Intron1]—[Exon2]—...—[3'UTR]—3'
```

**Components:**
- **Promoter:** Regulatory region where transcription begins
- **Exons:** Coding sequences retained in mature mRNA
- **Introns:** Non-coding sequences removed by splicing
- **UTRs:** Untranslated regions (5' and 3')

**Alleles:** Different versions of a gene
- Wild-type: most common allele
- Mutant: altered allele

**Gene expression:**
$$\\text{Gene} \\xrightarrow{\\text{transcription}} \\text{pre-mRNA} \\xrightarrow{\\text{splicing}} \\text{mRNA} \\xrightarrow{\\text{translation}} \\text{Protein}$$

**Human genome:** ~20,000-25,000 protein-coding genes""",
        "domain": "BIOLOGY",
        "subfield": "genetics",
        "complexity_level": 0,
        "is_axiom": False,
        "books": [
            "Molecular Biology of the Cell - Alberts et al., Ch. 6",
            "Genetics: Analysis and Principles - Brooker, Ch. 12",
        ],
        "prerequisites": ["DNA"],
    },
    # ==========================================================================
    # GENETIC CODE - Level 1
    # ==========================================================================
    {
        "name": "Codon",
        "definition_md": """## Codon

A **codon** is a sequence of three nucleotides in mRNA that specifies an amino acid
or a stop signal during translation:

**Structure:**
$$\\text{Codon} = \\text{(base}_1\\text{)(base}_2\\text{)(base}_3\\text{)}$$

where each base $\\in \\{\\text{A, U, G, C}\\}$

**Total codons:** $4^3 = 64$

**Genetic code:**
- **61 sense codons:** Encode 20 amino acids
- **3 stop codons:** UAA (ochre), UAG (amber), UGA (opal)
- **1 start codon:** AUG (also codes for methionine)

**Degeneracy:** Most amino acids have multiple codons
- Leucine: 6 codons (UUA, UUG, CUU, CUC, CUA, CUG)
- Methionine: 1 codon (AUG)
- Tryptophan: 1 codon (UGG)

**Wobble hypothesis:** Third codon position allows non-standard base pairing,
explaining degeneracy.

**Reading frame:** Codons are read consecutively without gaps
$$\\text{...AUG-GCC-UAA...}$$

**Universality:** The genetic code is nearly universal across all life.""",
        "domain": "BIOLOGY",
        "subfield": "molecular",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Molecular Biology of the Cell - Alberts et al., Ch. 6",
            "Molecular Biology of the Gene - Watson et al., Ch. 15",
        ],
        "prerequisites": ["Gene", "Central Dogma of Molecular Biology"],
    },
    {
        "name": "Protein",
        "definition_md": """## Protein

A **protein** is a macromolecule composed of one or more polypeptide chains:

**Composition:**
- Linear polymer of amino acids
- Peptide bonds link amino acids: $\\text{-CO-NH-}$
- 20 standard amino acids

**Amino acid structure:**
$$\\text{H}_2\\text{N}-\\text{C}_\\alpha\\text{H}(\\text{R})-\\text{COOH}$$

**Structural levels:**

1. **Primary:** Amino acid sequence
   $$\\text{Met-Ala-Gly-...}$$

2. **Secondary:** Local folding patterns
   - $\\alpha$-helix: Right-handed coil, 3.6 residues/turn
   - $\\beta$-sheet: Parallel or antiparallel strands

3. **Tertiary:** Overall 3D structure of single polypeptide
   - Stabilized by hydrophobic interactions, H-bonds, disulfide bonds

4. **Quaternary:** Multiple polypeptide chains
   - Example: Hemoglobin ($\\alpha_2\\beta_2$)

**Functions:**
- Enzymes (catalysis)
- Structural (collagen, keratin)
- Transport (hemoglobin)
- Signaling (hormones, receptors)""",
        "domain": "BIOLOGY",
        "subfield": "molecular",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Molecular Biology of the Cell - Alberts et al., Ch. 3",
            "Biochemistry - Stryer et al., Ch. 2-3",
        ],
        "prerequisites": ["Codon", "Central Dogma of Molecular Biology"],
    },
    # ==========================================================================
    # MENDELIAN GENETICS - Level 0 (Foundational)
    # ==========================================================================
    {
        "name": "Mendel's First Law",
        "definition_md": """## Mendel's First Law (Law of Segregation)

During gamete formation, the two alleles for each gene segregate so that each
gamete carries only one allele:

**Statement:** The two alleles of a gene separate during meiosis, with each
gamete receiving one allele.

**Molecular basis:** Homologous chromosomes separate during Meiosis I.

**Monohybrid cross:**
$$\\text{Aa} \\times \\text{Aa}$$

**Gametes:**
- Parent 1: $\\frac{1}{2}$A, $\\frac{1}{2}$a
- Parent 2: $\\frac{1}{2}$A, $\\frac{1}{2}$a

**Punnett square:**
|   | A | a |
|---|---|---|
| A | AA | Aa |
| a | Aa | aa |

**Offspring ratios:**
- Genotype: $\\frac{1}{4}$AA : $\\frac{2}{4}$Aa : $\\frac{1}{4}$aa = 1:2:1
- Phenotype (A dominant): $\\frac{3}{4}$dominant : $\\frac{1}{4}$recessive = 3:1

**Test cross:** Cross with homozygous recessive (aa) to determine genotype.""",
        "domain": "BIOLOGY",
        "subfield": "genetics",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Genetics: Analysis and Principles - Brooker, Ch. 2",
            "Campbell Biology - Ch. 14",
            "Genetics - Hartl & Jones, Ch. 2",
        ],
        "prerequisites": ["Gene"],
    },
    {
        "name": "Mendel's Second Law",
        "definition_md": """## Mendel's Second Law (Law of Independent Assortment)

Genes for different traits assort independently during gamete formation
(when genes are on different chromosomes):

**Statement:** Alleles of different genes are distributed independently of one
another during gamete formation.

**Molecular basis:** Non-homologous chromosomes align randomly at metaphase I.

**Dihybrid cross:**
$$\\text{AaBb} \\times \\text{AaBb}$$

**Gametes:** AB, Ab, aB, ab (each $\\frac{1}{4}$)

**Offspring phenotype ratio:** 9:3:3:1
- 9/16 A_B_ (both dominant)
- 3/16 A_bb (A dominant, b recessive)
- 3/16 aaB_ (a recessive, B dominant)
- 1/16 aabb (both recessive)

**Limitation:** Only applies when genes are on different chromosomes or far
apart on the same chromosome (unlinked genes).

**Linked genes:** Genes on the same chromosome may not assort independently;
recombination frequency measures genetic distance.

**Chi-square test:** Statistical test to compare observed vs. expected ratios:
$$\\chi^2 = \\sum \\frac{(O - E)^2}{E}$$""",
        "domain": "BIOLOGY",
        "subfield": "genetics",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Genetics: Analysis and Principles - Brooker, Ch. 2",
            "Campbell Biology - Ch. 14",
        ],
        "prerequisites": ["Mendel's First Law"],
    },
    # ==========================================================================
    # EVOLUTION - Level 0 (Foundational)
    # ==========================================================================
    {
        "name": "Natural Selection",
        "definition_md": """## Natural Selection

**Natural selection** is the differential survival and reproduction of individuals
due to differences in phenotype:

**Darwin's four postulates:**
1. **Variation:** Individuals in a population vary in their traits
2. **Heritability:** Some variation is heritable (passed to offspring)
3. **Competition:** More offspring are produced than can survive
4. **Differential success:** Individuals with favorable traits survive and reproduce more

**Fitness ($w$):** Relative reproductive success
$$w = \\frac{\\text{offspring of genotype}}{\\text{offspring of fittest genotype}}$$

**Selection coefficient ($s$):**
$$s = 1 - w$$

**Types of selection:**
- **Directional:** Favors one extreme phenotype
- **Stabilizing:** Favors intermediate phenotype
- **Disruptive:** Favors both extremes

**Hardy-Weinberg equilibrium (null model):**
$$p^2 + 2pq + q^2 = 1$$
where $p$ = frequency of dominant allele, $q$ = frequency of recessive allele.

**Evolution occurs when:** Allele frequencies change over generations.""",
        "domain": "BIOLOGY",
        "subfield": "evolution",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Evolution - Futuyma & Kirkpatrick, Ch. 3",
            "Campbell Biology - Ch. 23",
            "The Origin of Species - Darwin, Ch. 4",
        ],
        "prerequisites": ["Gene", "Mendel's First Law"],
    },
    # ==========================================================================
    # METABOLISM - Level 1
    # ==========================================================================
    {
        "name": "ATP",
        "definition_md": """## ATP (Adenosine Triphosphate)

**ATP** is the primary energy currency of cells:

**Structure:**
- Adenine base
- Ribose sugar
- Three phosphate groups

$$\\text{Adenine}-\\text{Ribose}-\\text{P}_\\alpha-\\text{P}_\\beta-\\text{P}_\\gamma$$

**Energy release:**
$$\\text{ATP} + \\text{H}_2\\text{O} \\to \\text{ADP} + \\text{P}_i + \\text{Energy}$$
$$\\Delta G^\\circ = -30.5 \\text{ kJ/mol}$$

**ATP synthesis:**
1. **Substrate-level phosphorylation:** Direct transfer of phosphate
   $$\\text{ADP} + \\text{P}_i \\to \\text{ATP}$$

2. **Oxidative phosphorylation:** Electron transport chain + chemiosmosis
   - ATP synthase uses proton gradient
   - ~30-32 ATP per glucose in aerobic respiration

**Uses of ATP:**
- Biosynthesis (anabolic reactions)
- Active transport (pumps)
- Mechanical work (muscle contraction)
- Signal transduction

**ATP turnover:** ~40 kg ATP recycled per day in humans.""",
        "domain": "BIOLOGY",
        "subfield": "biochemistry",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Molecular Biology of the Cell - Alberts et al., Ch. 2",
            "Biochemistry - Stryer et al., Ch. 14",
        ],
        "prerequisites": ["Cell"],
    },
    {
        "name": "Enzyme",
        "definition_md": """## Enzyme

An **enzyme** is a biological catalyst that accelerates chemical reactions:

**Properties:**
- Usually proteins (some RNA = ribozymes)
- Highly specific for substrates
- Not consumed in the reaction
- Lower activation energy ($E_a$)

**Michaelis-Menten kinetics:**
$$v = \\frac{V_{max}[S]}{K_m + [S]}$$

where:
- $v$ = reaction velocity
- $V_{max}$ = maximum velocity
- $[S]$ = substrate concentration
- $K_m$ = Michaelis constant (substrate concentration at $v = V_{max}/2$)

**Catalytic efficiency:**
$$\\frac{k_{cat}}{K_m}$$
where $k_{cat} = V_{max}/[E]_T$ (turnover number)

**Enzyme regulation:**
- **Competitive inhibition:** Inhibitor binds active site
- **Noncompetitive inhibition:** Inhibitor binds elsewhere
- **Allosteric regulation:** Binding at regulatory site changes activity
- **Covalent modification:** Phosphorylation, etc.

**Cofactors:** Non-protein components required for activity
- **Coenzymes:** Organic (NAD$^+$, FAD)
- **Metal ions:** Mg$^{2+}$, Zn$^{2+}$""",
        "domain": "BIOLOGY",
        "subfield": "biochemistry",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Biochemistry - Stryer et al., Ch. 8",
            "Molecular Biology of the Cell - Alberts et al., Ch. 3",
        ],
        "prerequisites": ["Protein", "ATP"],
    },
    # ==========================================================================
    # CELLULAR RESPIRATION - Level 1
    # ==========================================================================
    {
        "name": "Cellular Respiration",
        "definition_md": """## Cellular Respiration

**Cellular respiration** is the process of extracting energy from glucose:

**Overall reaction:**
$$\\text{C}_6\\text{H}_{12}\\text{O}_6 + 6\\text{O}_2 \\to 6\\text{CO}_2 + 6\\text{H}_2\\text{O} + \\text{ATP}$$
$$\\Delta G^\\circ = -2870 \\text{ kJ/mol}$$

**Stages:**

1. **Glycolysis** (cytoplasm):
   $$\\text{Glucose} \\to 2 \\text{ Pyruvate} + 2 \\text{ ATP} + 2 \\text{ NADH}$$

2. **Pyruvate oxidation** (mitochondrial matrix):
   $$\\text{Pyruvate} \\to \\text{Acetyl-CoA} + \\text{CO}_2 + \\text{NADH}$$

3. **Citric acid cycle** (mitochondrial matrix):
   $$\\text{Acetyl-CoA} \\to 2\\text{CO}_2 + 3\\text{NADH} + \\text{FADH}_2 + \\text{GTP}$$

4. **Oxidative phosphorylation** (inner mitochondrial membrane):
   $$\\text{NADH} + \\text{FADH}_2 + \\text{O}_2 \\to \\text{ATP} + \\text{H}_2\\text{O}$$

**ATP yield:** ~30-32 ATP per glucose (theoretical maximum)

**Anaerobic respiration:**
- Fermentation when O$_2$ unavailable
- Lactic acid fermentation or alcoholic fermentation""",
        "domain": "BIOLOGY",
        "subfield": "biochemistry",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Biochemistry - Stryer et al., Ch. 16-18",
            "Campbell Biology - Ch. 9",
            "Molecular Biology of the Cell - Alberts et al., Ch. 13",
        ],
        "prerequisites": ["ATP", "Enzyme", "Cell"],
    },
]
