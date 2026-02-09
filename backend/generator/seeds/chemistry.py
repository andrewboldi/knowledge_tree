"""Chemistry seed definitions - fundamental concepts and laws.

This module contains formal definitions of foundational chemistry concepts,
from atomic theory to thermodynamics and chemical bonding.
Each definition includes:
- name: The canonical name of the concept
- definition_md: Formal definition in Markdown with LaTeX notation
- domain: Always "CHEMISTRY" for this module
- subfield: The chemistry subfield (e.g., "general", "organic", "physical")
- complexity_level: 0 for fundamental laws/concepts, higher for derived
- is_axiom: True for fundamental postulates/laws
- books: Reference texts where the concept is covered
- prerequisites: List of concept names that must be understood first
"""

CHEMISTRY_AXIOM_DEFINITIONS = [
    # ==========================================================================
    # ATOMIC THEORY - Level 0 (Foundational)
    # ==========================================================================
    {
        "name": "Dalton's Atomic Theory",
        "definition_md": """## Dalton's Atomic Theory

Matter is composed of indivisible particles called **atoms**:

1. All matter consists of atoms, which are indivisible and indestructible
2. All atoms of a given element are identical in mass and properties
3. Compounds are formed by combinations of atoms of different elements
4. A chemical reaction involves rearrangement of atoms

**Law of Conservation of Mass:**
$$m_{reactants} = m_{products}$$

**Law of Definite Proportions:** A compound always contains the same elements
in the same mass ratios.

**Law of Multiple Proportions:** When two elements form multiple compounds,
the ratios of masses of one element that combine with a fixed mass of the
other are small whole numbers.

**Modern refinements:**
- Atoms are divisible (into protons, neutrons, electrons)
- Isotopes: atoms of same element can have different masses
- Atoms can be created/destroyed (nuclear reactions)""",
        "domain": "CHEMISTRY",
        "subfield": "general",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 2",
            "General Chemistry - Pauling, Ch. 1",
        ],
        "prerequisites": [],
    },
    {
        "name": "Atom",
        "definition_md": """## Atom

An **atom** is the smallest unit of an element that retains the chemical
properties of that element:

**Structure:**
- **Nucleus:** Dense center containing protons and neutrons
  - Proton: charge $+e$, mass $\\approx 1.673 \\times 10^{-27}$ kg
  - Neutron: charge $0$, mass $\\approx 1.675 \\times 10^{-27}$ kg
- **Electron cloud:** Electrons orbit the nucleus
  - Electron: charge $-e$, mass $\\approx 9.109 \\times 10^{-31}$ kg

**Atomic number:** $Z$ = number of protons (defines the element)

**Mass number:** $A$ = protons + neutrons

**Isotopes:** Atoms with same $Z$ but different $A$

**Notation:** $^A_Z X$ (e.g., $^{12}_6 C$ for carbon-12)

**Atomic radius:** Typically 1-3 Å ($10^{-10}$ m)

**Nuclear radius:** $r \\approx r_0 A^{1/3}$ where $r_0 \\approx 1.2$ fm""",
        "domain": "CHEMISTRY",
        "subfield": "general",
        "complexity_level": 0,
        "is_axiom": False,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 2",
            "Inorganic Chemistry - Shriver & Atkins, Ch. 1",
        ],
        "prerequisites": ["Dalton's Atomic Theory"],
    },
    {
        "name": "Mole",
        "definition_md": """## Mole

The **mole** (mol) is the SI unit of amount of substance, defined as exactly
$6.02214076 \\times 10^{23}$ elementary entities:

$$1 \\text{ mol} = 6.02214076 \\times 10^{23} \\text{ entities}$$

This number is **Avogadro's constant** $N_A$.

**Molar mass:** Mass of one mole of a substance
$$M = \\frac{m}{n} \\quad [\\text{g/mol}]$$

**Number of moles:**
$$n = \\frac{N}{N_A} = \\frac{m}{M}$$

where:
- $N$ is the number of entities
- $m$ is the mass
- $M$ is the molar mass

**Example:** One mole of $^{12}C$ has mass exactly 12 g.

**For gases at STP:** One mole occupies 22.4 L (ideal gas).

**Molar volume:**
$$V_m = \\frac{V}{n} = \\frac{RT}{P}$$""",
        "domain": "CHEMISTRY",
        "subfield": "general",
        "complexity_level": 0,
        "is_axiom": False,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 3",
            "General Chemistry - Pauling, Ch. 2",
        ],
        "prerequisites": ["Atom"],
    },
    # ==========================================================================
    # CHEMICAL BONDING - Level 1
    # ==========================================================================
    {
        "name": "Chemical Bond",
        "definition_md": """## Chemical Bond

A **chemical bond** is a lasting attraction between atoms that enables the
formation of molecules and compounds:

**Types of chemical bonds:**

1. **Ionic bond:** Transfer of electrons
   $$\\text{Na} + \\text{Cl} \\to \\text{Na}^+ + \\text{Cl}^-$$
   Energy: $E = \\frac{k_e q_1 q_2}{r}$ (Coulomb attraction)

2. **Covalent bond:** Sharing of electrons
   $$\\text{H} + \\text{H} \\to \\text{H}_2$$
   Electron density concentrated between nuclei

3. **Metallic bond:** Delocalized electrons
   Electrons shared among a lattice of metal cations

**Bond energy:** Energy required to break the bond (kJ/mol)

**Bond length:** Equilibrium distance between bonded nuclei (pm)

**Bond order:** Number of bonding electron pairs
$$\\text{Bond order} = \\frac{n_b - n_a}{2}$$
where $n_b$ = bonding electrons, $n_a$ = antibonding electrons""",
        "domain": "CHEMISTRY",
        "subfield": "general",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 8",
            "Inorganic Chemistry - Shriver & Atkins, Ch. 2",
        ],
        "prerequisites": ["Atom"],
    },
    {
        "name": "Electronegativity",
        "definition_md": """## Electronegativity

**Electronegativity** ($\\chi$) is a measure of an atom's ability to attract
bonding electrons:

**Pauling scale:** Most common scale, ranges from 0.7 (Cs) to 4.0 (F)

$$\\chi_A - \\chi_B = 0.102\\sqrt{\\Delta E} \\quad [\\text{eV}]$$

where $\\Delta E$ is the extra bond energy above the geometric mean.

**Mulliken scale:**
$$\\chi = \\frac{I + A}{2}$$
where $I$ = ionization energy, $A$ = electron affinity

**Trends in periodic table:**
- Increases left to right across a period
- Decreases down a group
- Noble gases traditionally excluded (low reactivity)

**Bond polarity:** $\\Delta\\chi > 0$ creates partial charges:
- $\\Delta\\chi < 0.5$: nonpolar covalent
- $0.5 < \\Delta\\chi < 1.7$: polar covalent
- $\\Delta\\chi > 1.7$: ionic

**Highly electronegative:** F (4.0), O (3.5), N (3.0), Cl (3.0)""",
        "domain": "CHEMISTRY",
        "subfield": "general",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 8",
            "Inorganic Chemistry - Shriver & Atkins, Ch. 2",
        ],
        "prerequisites": ["Chemical Bond"],
    },
    {
        "name": "Lewis Structure",
        "definition_md": """## Lewis Structure

A **Lewis structure** (electron dot structure) shows the bonding between atoms
and lone pairs of electrons:

**Rules for drawing:**
1. Count total valence electrons
2. Connect atoms with single bonds
3. Distribute remaining electrons as lone pairs (octets)
4. Form multiple bonds if needed for octets

**Octet rule:** Atoms tend to have 8 valence electrons (2 for H)

**Formal charge:**
$$\\text{FC} = V - L - \\frac{B}{2}$$
where $V$ = valence electrons, $L$ = lone pair electrons, $B$ = bonding electrons

**Resonance:** Multiple valid Lewis structures for one molecule
$$\\text{NO}_2^- : \\quad [\\text{O}=\\text{N}-\\text{O}]^- \\leftrightarrow [\\text{O}-\\text{N}=\\text{O}]^-$$

**Exceptions to octet:**
- Incomplete octet: BF$_3$ (6 electrons on B)
- Expanded octet: SF$_6$ (12 electrons on S)
- Odd-electron species: NO (11 electrons)""",
        "domain": "CHEMISTRY",
        "subfield": "general",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 8",
            "Organic Chemistry - Clayden et al., Ch. 1",
        ],
        "prerequisites": ["Chemical Bond", "Electronegativity"],
    },
    # ==========================================================================
    # CHEMICAL THERMODYNAMICS - Level 0 (Foundational)
    # ==========================================================================
    {
        "name": "Enthalpy",
        "definition_md": """## Enthalpy

**Enthalpy** ($H$) is a thermodynamic potential defined as:

$$H = U + PV$$

where $U$ is internal energy, $P$ is pressure, $V$ is volume.

**Change in enthalpy:**
$$\\Delta H = \\Delta U + P\\Delta V$$

At constant pressure:
$$\\Delta H = q_P$$
(heat absorbed at constant pressure)

**Standard enthalpy of formation** ($\\Delta H_f^\\circ$):
Enthalpy change when 1 mole of compound forms from elements in standard states.

**Hess's Law:**
$$\\Delta H_{rxn} = \\sum \\Delta H_f^\\circ (\\text{products}) - \\sum \\Delta H_f^\\circ (\\text{reactants})$$

**Sign convention:**
- $\\Delta H < 0$: exothermic (releases heat)
- $\\Delta H > 0$: endothermic (absorbs heat)

**Bond enthalpy:** Energy to break a bond (average values used)""",
        "domain": "CHEMISTRY",
        "subfield": "physical",
        "complexity_level": 0,
        "is_axiom": False,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 5",
            "Physical Chemistry - Atkins & de Paula, Ch. 2",
        ],
        "prerequisites": ["Mole"],
    },
    {
        "name": "Gibbs Free Energy",
        "definition_md": """## Gibbs Free Energy

The **Gibbs free energy** ($G$) determines spontaneity at constant $T$ and $P$:

$$G = H - TS$$

**Change in Gibbs energy:**
$$\\Delta G = \\Delta H - T\\Delta S$$

**Spontaneity criterion:**
- $\\Delta G < 0$: spontaneous (thermodynamically favorable)
- $\\Delta G = 0$: equilibrium
- $\\Delta G > 0$: non-spontaneous

**Standard Gibbs energy:**
$$\\Delta G^\\circ = \\Delta H^\\circ - T\\Delta S^\\circ$$

**Relationship to equilibrium constant:**
$$\\Delta G^\\circ = -RT \\ln K$$

**Non-standard conditions:**
$$\\Delta G = \\Delta G^\\circ + RT \\ln Q$$
where $Q$ is the reaction quotient.

**Maximum non-expansion work:**
$$w_{max} = \\Delta G$$""",
        "domain": "CHEMISTRY",
        "subfield": "physical",
        "complexity_level": 0,
        "is_axiom": False,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 19",
            "Physical Chemistry - Atkins & de Paula, Ch. 3",
        ],
        "prerequisites": ["Enthalpy"],
    },
    {
        "name": "Chemical Equilibrium",
        "definition_md": """## Chemical Equilibrium

**Chemical equilibrium** is the state where forward and reverse reaction rates
are equal, with no net change in concentrations:

$$\\text{rate}_{forward} = \\text{rate}_{reverse}$$

**Equilibrium constant** ($K$):
For $aA + bB \\rightleftharpoons cC + dD$:

$$K = \\frac{[C]^c[D]^d}{[A]^a[B]^b}$$

**Relationship to Gibbs energy:**
$$\\Delta G^\\circ = -RT \\ln K$$

**Le Chatelier's Principle:** A system at equilibrium responds to stress by
shifting to counteract it:
- Add reactants $\\to$ shift right
- Increase pressure $\\to$ shift toward fewer moles of gas
- Increase temperature: shift toward endothermic direction

**Reaction quotient** ($Q$): Same expression as $K$, but not at equilibrium
- $Q < K$: reaction proceeds forward
- $Q > K$: reaction proceeds reverse
- $Q = K$: at equilibrium""",
        "domain": "CHEMISTRY",
        "subfield": "physical",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 15",
            "Physical Chemistry - Atkins & de Paula, Ch. 6",
        ],
        "prerequisites": ["Gibbs Free Energy"],
    },
    # ==========================================================================
    # ACIDS AND BASES - Level 1
    # ==========================================================================
    {
        "name": "Arrhenius Acid-Base Theory",
        "definition_md": """## Arrhenius Acid-Base Theory

**Arrhenius acid:** A substance that produces $\\text{H}^+$ ions in aqueous solution
$$\\text{HCl} \\to \\text{H}^+ + \\text{Cl}^-$$

**Arrhenius base:** A substance that produces $\\text{OH}^-$ ions in aqueous solution
$$\\text{NaOH} \\to \\text{Na}^+ + \\text{OH}^-$$

**Neutralization:**
$$\\text{H}^+ + \\text{OH}^- \\to \\text{H}_2\\text{O}$$

**Limitations:**
- Only applies to aqueous solutions
- Cannot explain bases like NH$_3$ that don't contain OH
- H$^+$ doesn't exist free; actually H$_3$O$^+$ (hydronium)

**pH scale:**
$$\\text{pH} = -\\log[\\text{H}^+]$$
$$\\text{pOH} = -\\log[\\text{OH}^-]$$
$$\\text{pH} + \\text{pOH} = 14 \\quad (\\text{at } 25°\\text{C})$$

**Water autoionization:**
$$K_w = [\\text{H}^+][\\text{OH}^-] = 10^{-14}$$""",
        "domain": "CHEMISTRY",
        "subfield": "general",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 16",
            "General Chemistry - Pauling, Ch. 15",
        ],
        "prerequisites": ["Mole", "Chemical Equilibrium"],
    },
    {
        "name": "Bronsted-Lowry Acid-Base Theory",
        "definition_md": """## Bronsted-Lowry Acid-Base Theory

**Bronsted-Lowry acid:** A proton (H$^+$) donor
**Bronsted-Lowry base:** A proton (H$^+$) acceptor

$$\\text{HA} + \\text{B} \\rightleftharpoons \\text{A}^- + \\text{HB}^+$$
(acid)   (base)    (conjugate base)  (conjugate acid)

**Conjugate acid-base pairs:** Differ by one proton
$$\\text{NH}_3 / \\text{NH}_4^+ \\quad \\text{H}_2\\text{O} / \\text{OH}^-$$

**Amphoteric substances:** Can act as acid or base
$$\\text{H}_2\\text{O} + \\text{H}_2\\text{O} \\rightleftharpoons \\text{H}_3\\text{O}^+ + \\text{OH}^-$$

**Acid dissociation constant:**
$$K_a = \\frac{[\\text{A}^-][\\text{H}_3\\text{O}^+]}{[\\text{HA}]}$$

**Base dissociation constant:**
$$K_b = \\frac{[\\text{HB}^+][\\text{OH}^-]}{[\\text{B}]}$$

**Relationship:**
$$K_a \\times K_b = K_w$$""",
        "domain": "CHEMISTRY",
        "subfield": "general",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 16",
            "Physical Chemistry - Atkins & de Paula, Ch. 6",
        ],
        "prerequisites": ["Arrhenius Acid-Base Theory"],
    },
    # ==========================================================================
    # OXIDATION-REDUCTION - Level 1
    # ==========================================================================
    {
        "name": "Oxidation State",
        "definition_md": """## Oxidation State

The **oxidation state** (oxidation number) is the hypothetical charge an atom
would have if all bonds were ionic:

**Rules for assigning oxidation states:**
1. Free elements: 0
2. Monatomic ions: equal to charge
3. Oxygen: usually $-2$ (except peroxides: $-1$)
4. Hydrogen: usually $+1$ (except metal hydrides: $-1$)
5. Halogens: usually $-1$
6. Sum in neutral molecule: 0
7. Sum in ion: equals charge

**Examples:**
- $\\text{H}_2\\text{O}$: H is $+1$, O is $-2$
- $\\text{MnO}_4^-$: O is $-2$, Mn is $+7$
- $\\text{Fe}_2\\text{O}_3$: O is $-2$, Fe is $+3$

**Change in oxidation state:**
- **Oxidation:** increase in oxidation state (loss of electrons)
- **Reduction:** decrease in oxidation state (gain of electrons)

**OIL RIG:** Oxidation Is Loss, Reduction Is Gain (of electrons)""",
        "domain": "CHEMISTRY",
        "subfield": "general",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 20",
            "Inorganic Chemistry - Shriver & Atkins, Ch. 5",
        ],
        "prerequisites": ["Chemical Bond", "Electronegativity"],
    },
    {
        "name": "Electrochemical Cell",
        "definition_md": """## Electrochemical Cell

An **electrochemical cell** converts chemical energy to electrical energy
(galvanic/voltaic) or vice versa (electrolytic):

**Galvanic cell components:**
- **Anode:** Oxidation occurs (negative terminal)
- **Cathode:** Reduction occurs (positive terminal)
- **Salt bridge:** Maintains electrical neutrality

**Cell notation:**
$$\\text{Zn}(s)|\\text{Zn}^{2+}(aq)||\\text{Cu}^{2+}(aq)|\\text{Cu}(s)$$

**Cell potential:**
$$E^\\circ_{cell} = E^\\circ_{cathode} - E^\\circ_{anode}$$

**Nernst equation:**
$$E = E^\\circ - \\frac{RT}{nF}\\ln Q = E^\\circ - \\frac{0.0592}{n}\\log Q \\quad (25°\\text{C})$$

**Relationship to Gibbs energy:**
$$\\Delta G^\\circ = -nFE^\\circ$$

where:
- $n$ = moles of electrons transferred
- $F = 96485$ C/mol (Faraday constant)

**Standard hydrogen electrode (SHE):** Reference electrode, $E^\\circ = 0$ V""",
        "domain": "CHEMISTRY",
        "subfield": "physical",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 20",
            "Physical Chemistry - Atkins & de Paula, Ch. 6",
        ],
        "prerequisites": ["Oxidation State", "Gibbs Free Energy"],
    },
    # ==========================================================================
    # REACTION KINETICS - Level 1
    # ==========================================================================
    {
        "name": "Reaction Rate",
        "definition_md": """## Reaction Rate

The **reaction rate** is the change in concentration of a reactant or product
per unit time:

For $aA + bB \\to cC + dD$:

$$\\text{rate} = -\\frac{1}{a}\\frac{d[A]}{dt} = -\\frac{1}{b}\\frac{d[B]}{dt} = \\frac{1}{c}\\frac{d[C]}{dt} = \\frac{1}{d}\\frac{d[D]}{dt}$$

**Rate law:**
$$\\text{rate} = k[A]^m[B]^n$$

where:
- $k$ = rate constant
- $m, n$ = reaction orders (determined experimentally)
- Overall order = $m + n$

**Integrated rate laws:**
- Zero order: $[A] = [A]_0 - kt$
- First order: $\\ln[A] = \\ln[A]_0 - kt$, $t_{1/2} = \\frac{\\ln 2}{k}$
- Second order: $\\frac{1}{[A]} = \\frac{1}{[A]_0} + kt$

**Temperature dependence (Arrhenius equation):**
$$k = Ae^{-E_a/RT}$$
where $E_a$ = activation energy, $A$ = pre-exponential factor""",
        "domain": "CHEMISTRY",
        "subfield": "physical",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 14",
            "Physical Chemistry - Atkins & de Paula, Ch. 20",
        ],
        "prerequisites": ["Mole", "Chemical Equilibrium"],
    },
    {
        "name": "Activation Energy",
        "definition_md": """## Activation Energy

The **activation energy** ($E_a$) is the minimum energy required for a reaction
to occur:

$$E_a = E_{\\text{transition state}} - E_{\\text{reactants}}$$

**Arrhenius equation:**
$$k = Ae^{-E_a/RT}$$

Taking the logarithm:
$$\\ln k = \\ln A - \\frac{E_a}{RT}$$

**Two-point form:**
$$\\ln\\frac{k_2}{k_1} = \\frac{E_a}{R}\\left(\\frac{1}{T_1} - \\frac{1}{T_2}\\right)$$

**Transition state theory:**
- Reactants must pass through a high-energy transition state
- The transition state is a maximum on the potential energy surface
- Products are more stable if $\\Delta H < 0$

**Catalysis:** Lowers $E_a$ by providing an alternative reaction pathway
- Catalyst is not consumed
- Increases rate but doesn't affect equilibrium position""",
        "domain": "CHEMISTRY",
        "subfield": "physical",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Chemistry: The Central Science - Brown et al., Ch. 14",
            "Physical Chemistry - Atkins & de Paula, Ch. 20",
        ],
        "prerequisites": ["Reaction Rate"],
    },
]
