"""Physics seed definitions - fundamental laws and concepts.

This module contains formal definitions of foundational physics concepts,
starting from Newtonian mechanics and extending to electromagnetism and thermodynamics.
Each definition includes:
- name: The canonical name of the concept
- definition_md: Formal definition in Markdown with LaTeX notation
- domain: Always "PHYSICS" for this module
- subfield: The physics subfield (e.g., "mechanics", "electromagnetism")
- complexity_level: 0 for fundamental laws, higher for derived concepts
- is_axiom: True for fundamental postulates/laws
- books: Reference texts where the concept is covered
- prerequisites: List of concept names that must be understood first
"""

PHYSICS_AXIOM_DEFINITIONS = [
    # ==========================================================================
    # NEWTONIAN MECHANICS - Level 0 (Foundational)
    # ==========================================================================
    {
        "name": "Newton's First Law",
        "definition_md": """## Newton's First Law (Law of Inertia)

An object at rest remains at rest, and an object in motion continues in motion
with constant velocity, unless acted upon by a net external force:

$$\\sum \\mathbf{F} = 0 \\implies \\frac{d\\mathbf{v}}{dt} = 0$$

**Formal statement:** In an inertial reference frame, if the net force $\\mathbf{F}_{net}$
on an object is zero, then its velocity $\\mathbf{v}$ is constant.

**Inertia:** The property of matter that resists changes in motion. Mass $m$ is the
quantitative measure of inertia.

**Inertial reference frame:** A frame in which Newton's first law holds. Any frame
moving at constant velocity relative to an inertial frame is also inertial.

**Note:** This law defines what force does (changes motion) and what an inertial
frame is (where isolated objects don't accelerate).""",
        "domain": "PHYSICS",
        "subfield": "mechanics",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Classical Mechanics - Goldstein, Ch. 1",
            "The Feynman Lectures on Physics - Vol. 1, Ch. 9",
            "Principles of Physics - Halliday, Resnick & Walker, Ch. 5",
        ],
        "prerequisites": [],
    },
    {
        "name": "Newton's Second Law",
        "definition_md": """## Newton's Second Law

The rate of change of momentum of an object equals the net force acting on it:

$$\\mathbf{F} = \\frac{d\\mathbf{p}}{dt} = \\frac{d(m\\mathbf{v})}{dt}$$

For constant mass:

$$\\mathbf{F} = m\\mathbf{a}$$

where:
- $\\mathbf{F}$ is the net force (N = kg$\\cdot$m/s$^2$)
- $m$ is the mass (kg)
- $\\mathbf{a} = d\\mathbf{v}/dt$ is the acceleration (m/s$^2$)
- $\\mathbf{p} = m\\mathbf{v}$ is the momentum (kg$\\cdot$m/s)

**Vector form:** This is a vector equation; each component satisfies:
$$F_x = ma_x, \\quad F_y = ma_y, \\quad F_z = ma_z$$

**Differential equation:** Given $\\mathbf{F}(\\mathbf{r}, \\mathbf{v}, t)$, this becomes
a second-order ODE determining the trajectory $\\mathbf{r}(t)$.""",
        "domain": "PHYSICS",
        "subfield": "mechanics",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Classical Mechanics - Goldstein, Ch. 1",
            "The Feynman Lectures on Physics - Vol. 1, Ch. 9",
            "Mechanics - Landau & Lifshitz, Ch. 1",
        ],
        "prerequisites": ["Newton's First Law"],
    },
    {
        "name": "Newton's Third Law",
        "definition_md": """## Newton's Third Law

For every action, there is an equal and opposite reaction:

$$\\mathbf{F}_{12} = -\\mathbf{F}_{21}$$

If object 1 exerts a force $\\mathbf{F}_{12}$ on object 2, then object 2 exerts
a force $\\mathbf{F}_{21} = -\\mathbf{F}_{12}$ on object 1.

**Key properties:**
- Forces always occur in pairs
- Action-reaction pairs act on **different** objects
- The forces are equal in magnitude, opposite in direction
- They act along the line connecting the objects (for contact forces)

**Consequence - Conservation of momentum:** For an isolated system:
$$\\frac{d}{dt}(\\mathbf{p}_1 + \\mathbf{p}_2) = \\mathbf{F}_{12} + \\mathbf{F}_{21} = 0$$

**Note:** The third law fails for electromagnetic forces between moving charges
(though momentum is still conserved when field momentum is included).""",
        "domain": "PHYSICS",
        "subfield": "mechanics",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Classical Mechanics - Goldstein, Ch. 1",
            "The Feynman Lectures on Physics - Vol. 1, Ch. 10",
        ],
        "prerequisites": ["Newton's Second Law"],
    },
    {
        "name": "Law of Universal Gravitation",
        "definition_md": """## Newton's Law of Universal Gravitation

Every point mass attracts every other point mass with a force directed along the
line connecting them, proportional to the product of their masses and inversely
proportional to the square of the distance:

$$\\mathbf{F} = -G\\frac{m_1 m_2}{r^2}\\hat{\\mathbf{r}}$$

where:
- $G = 6.674 \\times 10^{-11}$ N$\\cdot$m$^2$/kg$^2$ (gravitational constant)
- $m_1, m_2$ are the masses
- $r$ is the distance between centers
- $\\hat{\\mathbf{r}}$ is the unit vector from $m_1$ to $m_2$

**Gravitational field:**
$$\\mathbf{g} = -G\\frac{M}{r^2}\\hat{\\mathbf{r}}$$

**Gravitational potential energy:**
$$U = -G\\frac{m_1 m_2}{r}$$

**Shell theorem:** A uniform spherical shell exerts no gravitational force on a
particle inside it, and acts on external particles as if all mass were at the center.""",
        "domain": "PHYSICS",
        "subfield": "mechanics",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Classical Mechanics - Goldstein, Ch. 1",
            "Gravitation - Misner, Thorne & Wheeler, Ch. 1",
        ],
        "prerequisites": ["Newton's Second Law"],
    },
    # ==========================================================================
    # CONSERVATION LAWS - Level 1
    # ==========================================================================
    {
        "name": "Conservation of Energy",
        "definition_md": """## Conservation of Energy

The total energy of an isolated system remains constant:

$$E_{total} = K + U = \\text{constant}$$

where:
- $K = \\frac{1}{2}mv^2$ is kinetic energy
- $U$ is potential energy

**Work-Energy Theorem:**
$$W_{net} = \\Delta K = K_f - K_i$$

**Conservative forces:** A force $\\mathbf{F}$ is conservative if:
$$\\oint \\mathbf{F} \\cdot d\\mathbf{r} = 0$$
equivalently, $\\mathbf{F} = -\\nabla U$ for some potential $U$.

**First Law of Thermodynamics:**
$$\\Delta U = Q - W$$
where $Q$ is heat added and $W$ is work done by the system.

**Noether's Theorem:** Energy conservation follows from time-translation symmetry
of the laws of physics.""",
        "domain": "PHYSICS",
        "subfield": "mechanics",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Classical Mechanics - Goldstein, Ch. 2",
            "The Feynman Lectures on Physics - Vol. 1, Ch. 4",
        ],
        "prerequisites": ["Newton's Second Law"],
    },
    {
        "name": "Conservation of Momentum",
        "definition_md": """## Conservation of Momentum

The total momentum of an isolated system remains constant:

$$\\mathbf{p}_{total} = \\sum_i m_i \\mathbf{v}_i = \\text{constant}$$

**Derivation from Newton's Third Law:** For two particles:
$$\\frac{d\\mathbf{p}_1}{dt} + \\frac{d\\mathbf{p}_2}{dt} = \\mathbf{F}_{12} + \\mathbf{F}_{21} = 0$$

**Center of mass:**
$$\\mathbf{R}_{cm} = \\frac{\\sum_i m_i \\mathbf{r}_i}{\\sum_i m_i}$$

The center of mass moves at constant velocity for an isolated system.

**Impulse-Momentum Theorem:**
$$\\mathbf{J} = \\int \\mathbf{F} \\, dt = \\Delta \\mathbf{p}$$

**Noether's Theorem:** Momentum conservation follows from spatial translation
symmetry of the laws of physics.""",
        "domain": "PHYSICS",
        "subfield": "mechanics",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Classical Mechanics - Goldstein, Ch. 1",
            "The Feynman Lectures on Physics - Vol. 1, Ch. 10",
        ],
        "prerequisites": ["Newton's Third Law"],
    },
    {
        "name": "Conservation of Angular Momentum",
        "definition_md": """## Conservation of Angular Momentum

The total angular momentum of an isolated system remains constant when no
external torques act:

$$\\mathbf{L} = \\sum_i \\mathbf{r}_i \\times \\mathbf{p}_i = \\text{constant}$$

**Torque:**
$$\\boldsymbol{\\tau} = \\mathbf{r} \\times \\mathbf{F} = \\frac{d\\mathbf{L}}{dt}$$

**For rigid body rotation:**
$$L = I\\omega$$
where $I$ is the moment of inertia and $\\omega$ is angular velocity.

**Moment of inertia:**
$$I = \\sum_i m_i r_i^2 = \\int r^2 \\, dm$$

**Parallel axis theorem:**
$$I = I_{cm} + Md^2$$

**Noether's Theorem:** Angular momentum conservation follows from rotational
symmetry of the laws of physics.""",
        "domain": "PHYSICS",
        "subfield": "mechanics",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Classical Mechanics - Goldstein, Ch. 4",
            "The Feynman Lectures on Physics - Vol. 1, Ch. 18",
        ],
        "prerequisites": ["Conservation of Momentum"],
    },
    # ==========================================================================
    # ELECTROMAGNETISM - Level 0 (Foundational)
    # ==========================================================================
    {
        "name": "Coulomb's Law",
        "definition_md": """## Coulomb's Law

The electric force between two point charges is proportional to the product
of the charges and inversely proportional to the square of the distance:

$$\\mathbf{F} = k_e \\frac{q_1 q_2}{r^2} \\hat{\\mathbf{r}} = \\frac{1}{4\\pi\\epsilon_0} \\frac{q_1 q_2}{r^2} \\hat{\\mathbf{r}}$$

where:
- $k_e = 8.99 \\times 10^9$ N$\\cdot$m$^2$/C$^2$ (Coulomb constant)
- $\\epsilon_0 = 8.85 \\times 10^{-12}$ F/m (permittivity of free space)
- $q_1, q_2$ are the charges (C)
- $r$ is the distance between charges

**Electric field:**
$$\\mathbf{E} = \\frac{\\mathbf{F}}{q} = \\frac{1}{4\\pi\\epsilon_0} \\frac{Q}{r^2} \\hat{\\mathbf{r}}$$

**Superposition principle:** The total force on a charge is the vector sum
of forces from all other charges.

**Note:** Coulomb's law is the electrostatic limit of the full electromagnetic theory.""",
        "domain": "PHYSICS",
        "subfield": "electromagnetism",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Introduction to Electrodynamics - Griffiths, Ch. 2",
            "The Feynman Lectures on Physics - Vol. 2, Ch. 4",
        ],
        "prerequisites": [],
    },
    {
        "name": "Gauss's Law",
        "definition_md": """## Gauss's Law

The electric flux through any closed surface is proportional to the enclosed charge:

$$\\oint_S \\mathbf{E} \\cdot d\\mathbf{A} = \\frac{Q_{enc}}{\\epsilon_0}$$

**Differential form:**
$$\\nabla \\cdot \\mathbf{E} = \\frac{\\rho}{\\epsilon_0}$$

where $\\rho$ is the charge density.

**Applications:**
- Spherical symmetry: $E = \\frac{Q}{4\\pi\\epsilon_0 r^2}$
- Infinite line charge: $E = \\frac{\\lambda}{2\\pi\\epsilon_0 r}$
- Infinite plane: $E = \\frac{\\sigma}{2\\epsilon_0}$

**Gaussian surface:** An imaginary closed surface used to exploit symmetry.
Choose surfaces where $\\mathbf{E}$ is constant and perpendicular (or parallel) to $d\\mathbf{A}$.

**Note:** Gauss's law is one of Maxwell's equations.""",
        "domain": "PHYSICS",
        "subfield": "electromagnetism",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Introduction to Electrodynamics - Griffiths, Ch. 2",
            "Classical Electrodynamics - Jackson, Ch. 1",
        ],
        "prerequisites": ["Coulomb's Law"],
    },
    {
        "name": "Faraday's Law",
        "definition_md": """## Faraday's Law of Induction

A changing magnetic flux through a circuit induces an electromotive force (EMF):

$$\\mathcal{E} = -\\frac{d\\Phi_B}{dt}$$

where the magnetic flux is:
$$\\Phi_B = \\int_S \\mathbf{B} \\cdot d\\mathbf{A}$$

**Differential form (Maxwell-Faraday equation):**
$$\\nabla \\times \\mathbf{E} = -\\frac{\\partial \\mathbf{B}}{\\partial t}$$

**Lenz's Law:** The induced current flows in a direction to oppose the change
in flux (hence the negative sign).

**Applications:**
- Generators: Rotating coil in magnetic field
- Transformers: Changing current in primary induces EMF in secondary
- Inductance: Self-induced EMF opposes current change

**Note:** Faraday's law is one of Maxwell's equations and shows that changing
magnetic fields create electric fields.""",
        "domain": "PHYSICS",
        "subfield": "electromagnetism",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Introduction to Electrodynamics - Griffiths, Ch. 7",
            "The Feynman Lectures on Physics - Vol. 2, Ch. 17",
        ],
        "prerequisites": ["Gauss's Law"],
    },
    {
        "name": "Ampère-Maxwell Law",
        "definition_md": """## Ampère-Maxwell Law

Magnetic fields are produced by electric currents and changing electric fields:

$$\\oint_C \\mathbf{B} \\cdot d\\mathbf{l} = \\mu_0 I_{enc} + \\mu_0 \\epsilon_0 \\frac{d\\Phi_E}{dt}$$

**Differential form:**
$$\\nabla \\times \\mathbf{B} = \\mu_0 \\mathbf{J} + \\mu_0 \\epsilon_0 \\frac{\\partial \\mathbf{E}}{\\partial t}$$

where:
- $\\mu_0 = 4\\pi \\times 10^{-7}$ T$\\cdot$m/A (permeability of free space)
- $\\mathbf{J}$ is the current density
- The second term is Maxwell's **displacement current**

**Maxwell's insight:** The displacement current term $\\epsilon_0 \\partial \\mathbf{E}/\\partial t$
was added by Maxwell to ensure charge conservation and predicts electromagnetic waves.

**Speed of light:** $c = 1/\\sqrt{\\mu_0 \\epsilon_0}$

**Note:** Without the displacement current, Ampère's law would violate charge conservation.""",
        "domain": "PHYSICS",
        "subfield": "electromagnetism",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Introduction to Electrodynamics - Griffiths, Ch. 7",
            "Classical Electrodynamics - Jackson, Ch. 6",
        ],
        "prerequisites": ["Gauss's Law", "Faraday's Law"],
    },
    # ==========================================================================
    # THERMODYNAMICS - Level 0 (Foundational)
    # ==========================================================================
    {
        "name": "Zeroth Law of Thermodynamics",
        "definition_md": """## Zeroth Law of Thermodynamics

If two systems are each in thermal equilibrium with a third system, then they
are in thermal equilibrium with each other:

$$(A \\sim C) \\land (B \\sim C) \\implies A \\sim B$$

where $\\sim$ denotes thermal equilibrium.

**Consequence:** This law establishes temperature as a well-defined property.
Systems in thermal equilibrium have the same temperature.

**Thermal equilibrium:** Two systems are in thermal equilibrium if, when brought
into thermal contact, no net heat flows between them.

**Temperature:** A scalar quantity $T$ such that systems in thermal equilibrium
have the same value of $T$.

**Importance:** This law justifies the use of thermometers - if a thermometer
is in equilibrium with system A and reads the same as when in equilibrium with
system B, then A and B are in equilibrium with each other.""",
        "domain": "PHYSICS",
        "subfield": "thermodynamics",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Thermal Physics - Kittel & Kroemer, Ch. 1",
            "Thermodynamics - Fermi, Ch. 1",
        ],
        "prerequisites": [],
    },
    {
        "name": "First Law of Thermodynamics",
        "definition_md": """## First Law of Thermodynamics

Energy is conserved: the change in internal energy of a system equals the heat
added minus the work done by the system:

$$\\Delta U = Q - W$$

or in differential form:
$$dU = \\delta Q - \\delta W$$

where:
- $U$ is internal energy (a state function)
- $Q$ is heat added to the system
- $W$ is work done by the system
- $\\delta Q$ and $\\delta W$ are inexact differentials (path-dependent)

**For quasistatic processes:**
$$\\delta W = P \\, dV$$

**For ideal gas:**
$$dU = nC_V \\, dT$$

**Note:** $Q$ and $W$ individually depend on the process path, but $\\Delta U$
depends only on initial and final states.""",
        "domain": "PHYSICS",
        "subfield": "thermodynamics",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Thermal Physics - Kittel & Kroemer, Ch. 2",
            "Thermodynamics - Fermi, Ch. 2",
            "Statistical Mechanics - Pathria, Ch. 1",
        ],
        "prerequisites": ["Zeroth Law of Thermodynamics"],
    },
    {
        "name": "Second Law of Thermodynamics",
        "definition_md": """## Second Law of Thermodynamics

The total entropy of an isolated system never decreases:

$$\\Delta S_{total} \\geq 0$$

**Clausius statement:** Heat cannot spontaneously flow from a colder body to
a hotter body without external work.

**Kelvin-Planck statement:** No cyclic process can convert heat completely
into work without other effects.

**Entropy definition:**
$$dS = \\frac{\\delta Q_{rev}}{T}$$

**Entropy change for irreversible process:**
$$\\Delta S > \\int \\frac{\\delta Q}{T}$$

**Boltzmann entropy:**
$$S = k_B \\ln \\Omega$$
where $\\Omega$ is the number of microstates.

**Consequences:**
- Heat engines have efficiency $\\eta < 1$
- Carnot efficiency: $\\eta_{max} = 1 - T_C/T_H$
- Spontaneous processes increase total entropy""",
        "domain": "PHYSICS",
        "subfield": "thermodynamics",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Thermal Physics - Kittel & Kroemer, Ch. 2",
            "Thermodynamics - Fermi, Ch. 4",
            "Statistical Mechanics - Pathria, Ch. 1",
        ],
        "prerequisites": ["First Law of Thermodynamics"],
    },
    {
        "name": "Third Law of Thermodynamics",
        "definition_md": """## Third Law of Thermodynamics

The entropy of a perfect crystal approaches zero as temperature approaches
absolute zero:

$$\\lim_{T \\to 0} S = 0$$

**Nernst Heat Theorem:** The entropy change in any isothermal process approaches
zero as $T \\to 0$:
$$\\lim_{T \\to 0} \\Delta S = 0$$

**Consequences:**
- Absolute zero is unattainable in a finite number of steps
- Heat capacities vanish as $T \\to 0$: $C_V, C_P \\to 0$
- Provides an absolute reference for entropy (unlike energy)

**Statistical interpretation:** At $T = 0$, a perfect crystal has a unique
ground state, so $\\Omega = 1$ and $S = k_B \\ln 1 = 0$.

**Note:** For systems with degenerate ground states, $S(T=0) = k_B \\ln g$ where
$g$ is the ground state degeneracy.""",
        "domain": "PHYSICS",
        "subfield": "thermodynamics",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Thermal Physics - Kittel & Kroemer, Ch. 3",
            "Thermodynamics - Fermi, Ch. 8",
        ],
        "prerequisites": ["Second Law of Thermodynamics"],
    },
    # ==========================================================================
    # SPECIAL RELATIVITY - Level 1
    # ==========================================================================
    {
        "name": "Principle of Relativity",
        "definition_md": """## Principle of Relativity

The laws of physics are the same in all inertial reference frames:

$$\\text{If } \\mathcal{L}(\\mathbf{x}, \\dot{\\mathbf{x}}, t) \\text{ describes physics in frame } S,$$
$$\\text{then } \\mathcal{L}'(\\mathbf{x}', \\dot{\\mathbf{x}}', t') \\text{ has the same form in frame } S'$$

**Einstein's postulates (Special Relativity):**
1. The laws of physics are the same in all inertial frames
2. The speed of light $c$ is the same in all inertial frames

**Lorentz transformation:** For relative velocity $v$ along $x$:
$$x' = \\gamma(x - vt), \\quad t' = \\gamma(t - vx/c^2)$$
where $\\gamma = 1/\\sqrt{1 - v^2/c^2}$

**Consequences:**
- Time dilation: $\\Delta t' = \\gamma \\Delta t_0$
- Length contraction: $L = L_0/\\gamma$
- Relativity of simultaneity
- $E = mc^2$""",
        "domain": "PHYSICS",
        "subfield": "special_relativity",
        "complexity_level": 1,
        "is_axiom": True,
        "books": [
            "Spacetime Physics - Taylor & Wheeler",
            "Classical Electrodynamics - Jackson, Ch. 11",
            "The Feynman Lectures on Physics - Vol. 1, Ch. 15",
        ],
        "prerequisites": ["Newton's First Law"],
    },
    {
        "name": "Mass-Energy Equivalence",
        "definition_md": """## Mass-Energy Equivalence

Mass and energy are equivalent, related by:

$$E = mc^2$$

**Rest energy:** An object at rest has energy $E_0 = m_0 c^2$.

**Relativistic energy:**
$$E = \\gamma m_0 c^2 = \\frac{m_0 c^2}{\\sqrt{1 - v^2/c^2}}$$

**Energy-momentum relation:**
$$E^2 = (pc)^2 + (m_0 c^2)^2$$

**For photons:** $m_0 = 0$, so $E = pc$.

**Relativistic momentum:**
$$\\mathbf{p} = \\gamma m_0 \\mathbf{v}$$

**Kinetic energy:**
$$K = E - E_0 = (\\gamma - 1)m_0 c^2 \\approx \\frac{1}{2}m_0 v^2 \\text{ for } v \\ll c$$

**Note:** This equation explains nuclear energy: small mass deficits release
enormous energy.""",
        "domain": "PHYSICS",
        "subfield": "special_relativity",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Spacetime Physics - Taylor & Wheeler",
            "Introduction to Special Relativity - Rindler",
        ],
        "prerequisites": ["Principle of Relativity"],
    },
    # ==========================================================================
    # QUANTUM MECHANICS - Level 1
    # ==========================================================================
    {
        "name": "Wave-Particle Duality",
        "definition_md": """## Wave-Particle Duality

All matter exhibits both wave and particle properties:

**de Broglie relation:**
$$\\lambda = \\frac{h}{p} = \\frac{h}{mv}$$

where:
- $\\lambda$ is the de Broglie wavelength
- $h = 6.626 \\times 10^{-34}$ J$\\cdot$s (Planck's constant)
- $p$ is the momentum

**Photon energy:**
$$E = h\\nu = \\frac{hc}{\\lambda} = \\hbar\\omega$$

where $\\hbar = h/2\\pi$.

**Evidence:**
- **Wave behavior:** Diffraction and interference (double-slit experiment)
- **Particle behavior:** Photoelectric effect, Compton scattering

**Complementarity (Bohr):** Wave and particle descriptions are complementary;
the experimental setup determines which aspect is observed.

**Note:** This duality is fundamental to quantum mechanics and cannot be
explained by classical physics.""",
        "domain": "PHYSICS",
        "subfield": "quantum_mechanics",
        "complexity_level": 1,
        "is_axiom": True,
        "books": [
            "Principles of Quantum Mechanics - Shankar, Ch. 1",
            "Quantum Mechanics - Griffiths, Ch. 1",
            "The Feynman Lectures on Physics - Vol. 3, Ch. 1",
        ],
        "prerequisites": ["Principle of Relativity"],
    },
    {
        "name": "Heisenberg Uncertainty Principle",
        "definition_md": """## Heisenberg Uncertainty Principle

Certain pairs of physical properties cannot be simultaneously known with
arbitrary precision:

$$\\Delta x \\cdot \\Delta p \\geq \\frac{\\hbar}{2}$$

**General form:** For observables $A$ and $B$:
$$\\Delta A \\cdot \\Delta B \\geq \\frac{1}{2}|\\langle[\\hat{A}, \\hat{B}]\\rangle|$$

**Energy-time uncertainty:**
$$\\Delta E \\cdot \\Delta t \\geq \\frac{\\hbar}{2}$$

**Key pairs:**
- Position-momentum: $[\\hat{x}, \\hat{p}] = i\\hbar$
- Angular momentum components: $[\\hat{L}_x, \\hat{L}_y] = i\\hbar \\hat{L}_z$

**Interpretation:**
- Not a measurement limitation, but a fundamental property of nature
- Conjugate variables cannot have definite values simultaneously
- Wave function cannot have arbitrarily narrow spread in both $x$ and $p$

**Note:** This is not about disturbing the system during measurement, but about
the nature of quantum states themselves.""",
        "domain": "PHYSICS",
        "subfield": "quantum_mechanics",
        "complexity_level": 1,
        "is_axiom": True,
        "books": [
            "Principles of Quantum Mechanics - Shankar, Ch. 9",
            "Quantum Mechanics - Griffiths, Ch. 3",
        ],
        "prerequisites": ["Wave-Particle Duality"],
    },
    {
        "name": "Schrödinger Equation",
        "definition_md": """## Schrödinger Equation

The time evolution of a quantum system is governed by:

**Time-dependent Schrödinger equation:**
$$i\\hbar \\frac{\\partial \\Psi}{\\partial t} = \\hat{H}\\Psi$$

**Time-independent Schrödinger equation:**
$$\\hat{H}\\psi = E\\psi$$

where:
- $\\Psi(\\mathbf{r}, t)$ is the wave function
- $\\hat{H}$ is the Hamiltonian operator
- $E$ is the energy eigenvalue

**For a particle in a potential $V(\\mathbf{r})$:**
$$-\\frac{\\hbar^2}{2m}\\nabla^2\\Psi + V\\Psi = i\\hbar\\frac{\\partial\\Psi}{\\partial t}$$

**Probability interpretation (Born rule):**
$$|\\Psi(\\mathbf{r}, t)|^2 \\, d^3r = \\text{probability of finding particle in } d^3r$$

**Normalization:**
$$\\int |\\Psi|^2 \\, d^3r = 1$$

**Note:** The Schrödinger equation is deterministic; randomness enters only
through measurement.""",
        "domain": "PHYSICS",
        "subfield": "quantum_mechanics",
        "complexity_level": 1,
        "is_axiom": True,
        "books": [
            "Principles of Quantum Mechanics - Shankar, Ch. 4",
            "Quantum Mechanics - Griffiths, Ch. 1-2",
            "Modern Quantum Mechanics - Sakurai, Ch. 2",
        ],
        "prerequisites": ["Heisenberg Uncertainty Principle"],
    },
]
