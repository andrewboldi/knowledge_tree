"""Mathematics seed definitions - ZFC axioms and foundational set theory.

This module contains formal definitions of the Zermelo-Fraenkel axioms with the
Axiom of Choice (ZFC), which form the foundation of modern mathematics.
Each definition includes:
- name: The canonical name of the axiom or concept
- definition_md: Formal definition in Markdown with LaTeX notation
- domain: Always "MATH" for this module
- subfield: The mathematical subfield (e.g., "set_theory")
- complexity_level: 0 for axioms, higher for derived concepts
- is_axiom: True for axioms, False for derived definitions
- books: Reference texts where the concept is covered
- prerequisites: List of concept names that must be understood first
"""

MATH_AXIOM_DEFINITIONS = [
    # ==========================================================================
    # ZFC AXIOMS - Level 0 (Foundational)
    # ==========================================================================
    {
        "name": "Axiom of Extensionality",
        "definition_md": """## Axiom of Extensionality

Two sets are equal if and only if they contain exactly the same elements:

$$\\forall A \\forall B \\left( \\forall x (x \\in A \\iff x \\in B) \\implies A = B \\right)$$

**Informal:** Sets are determined entirely by their members. There is no notion
of "how" a set is defined or "when" it was created - only what elements it contains.

**Consequence:** This axiom establishes that set equality is extensional
(based on extension/membership) rather than intensional (based on definition).

**Example:** The sets $\\{1, 2, 3\\}$ and $\\{3, 1, 2\\}$ are equal because they
contain the same elements, despite being written differently.""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Naive Set Theory - Paul Halmos, Ch. 1",
            "Set Theory and Its Philosophy - Michael Potter, Ch. 3",
        ],
        "prerequisites": [],
    },
    {
        "name": "Axiom of Empty Set",
        "definition_md": """## Axiom of Empty Set

There exists a set with no elements:

$$\\exists A \\, \\forall x \\, (x \\notin A)$$

The **empty set** (or null set) is denoted $\\emptyset$ or $\\{\\}$.

**Uniqueness:** By the Axiom of Extensionality, the empty set is unique. If $A$
and $B$ are both sets with no elements, then $\\forall x (x \\in A \\iff x \\in B)$
is vacuously true, so $A = B$.

**Properties:**
- $\\emptyset \\subseteq X$ for any set $X$ (vacuously true)
- $|\\emptyset| = 0$ (cardinality is zero)
- $\\emptyset \\neq \\{\\emptyset\\}$ (the set containing the empty set is not empty)""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Naive Set Theory - Paul Halmos, Ch. 2",
        ],
        "prerequisites": ["Axiom of Extensionality"],
    },
    {
        "name": "Axiom of Pairing",
        "definition_md": """## Axiom of Pairing

For any two sets $a$ and $b$, there exists a set containing exactly $a$ and $b$:

$$\\forall a \\, \\forall b \\, \\exists C \\, \\forall x \\, (x \\in C \\iff x = a \\lor x = b)$$

This set $C$ is denoted $\\{a, b\\}$ and is called the **unordered pair** of $a$ and $b$.

**Special case:** When $a = b$, we get the **singleton** $\\{a\\} = \\{a, a\\}$.

**Note:** This axiom guarantees the existence of sets with exactly two elements.
Combined with other axioms, it enables the construction of finite sets of any size.

**Example:** Given sets $A = \\{1\\}$ and $B = \\{2\\}$, the axiom guarantees
$\\{A, B\\} = \\{\\{1\\}, \\{2\\}\\}$ exists.""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Naive Set Theory - Paul Halmos, Ch. 3",
        ],
        "prerequisites": ["Axiom of Extensionality"],
    },
    {
        "name": "Axiom of Union",
        "definition_md": """## Axiom of Union

For any set $\\mathcal{F}$ (a family of sets), there exists a set whose elements
are exactly those that belong to at least one member of $\\mathcal{F}$:

$$\\forall \\mathcal{F} \\, \\exists U \\, \\forall x \\, (x \\in U \\iff \\exists A \\in \\mathcal{F} \\, (x \\in A))$$

This set $U$ is called the **union** of $\\mathcal{F}$, denoted $\\bigcup \\mathcal{F}$.

**Binary union:** For two sets $A$ and $B$:
$$A \\cup B = \\bigcup \\{A, B\\} = \\{x : x \\in A \\lor x \\in B\\}$$

**Properties:**
- $A \\cup \\emptyset = A$
- $A \\cup A = A$ (idempotence)
- $A \\cup B = B \\cup A$ (commutativity)
- $(A \\cup B) \\cup C = A \\cup (B \\cup C)$ (associativity)""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Naive Set Theory - Paul Halmos, Ch. 4",
        ],
        "prerequisites": ["Axiom of Extensionality", "Axiom of Pairing"],
    },
    {
        "name": "Axiom of Power Set",
        "definition_md": """## Axiom of Power Set

For any set $A$, there exists a set whose elements are exactly the subsets of $A$:

$$\\forall A \\, \\exists P \\, \\forall X \\, (X \\in P \\iff X \\subseteq A)$$

This set $P$ is called the **power set** of $A$, denoted $\\mathcal{P}(A)$ or $2^A$.

**Cardinality:** If $|A| = n$ (finite), then $|\\mathcal{P}(A)| = 2^n$.

**Examples:**
- $\\mathcal{P}(\\emptyset) = \\{\\emptyset\\}$
- $\\mathcal{P}(\\{a\\}) = \\{\\emptyset, \\{a\\}\\}$
- $\\mathcal{P}(\\{a, b\\}) = \\{\\emptyset, \\{a\\}, \\{b\\}, \\{a, b\\}\\}$

**Important:** $\\emptyset \\in \\mathcal{P}(A)$ and $A \\in \\mathcal{P}(A)$ for any set $A$.

**Cantor's Theorem:** For any set $A$, $|A| < |\\mathcal{P}(A)|$ (strict inequality).""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Naive Set Theory - Paul Halmos, Ch. 5",
        ],
        "prerequisites": ["Axiom of Extensionality", "Subset"],
    },
    {
        "name": "Axiom Schema of Specification",
        "definition_md": """## Axiom Schema of Specification (Separation)

For any set $A$ and any property $\\varphi(x)$ expressible in the language of set theory,
there exists a set containing exactly those elements of $A$ that satisfy $\\varphi$:

$$\\forall A \\, \\exists B \\, \\forall x \\, (x \\in B \\iff x \\in A \\land \\varphi(x))$$

The resulting set is written $B = \\{x \\in A : \\varphi(x)\\}$.

**Why "Schema":** This is actually an infinite family of axioms, one for each formula $\\varphi$.

**Important:** We can only "separate" elements from an existing set $A$. This prevents
Russell's Paradox by not allowing the construction of $\\{x : x \\notin x\\}$ without
a bounding set.

**Examples:**
- $\\{n \\in \\mathbb{N} : n \\text{ is even}\\}$ (even natural numbers)
- $\\{x \\in \\mathbb{R} : x^2 < 2\\}$ (reals with square less than 2)""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Naive Set Theory - Paul Halmos, Ch. 2",
            "Elements of Set Theory - Herbert Enderton, Ch. 2",
        ],
        "prerequisites": ["Axiom of Extensionality"],
    },
    {
        "name": "Axiom of Infinity",
        "definition_md": """## Axiom of Infinity

There exists a set that contains $\\emptyset$ and is closed under the successor operation:

$$\\exists I \\, \\left( \\emptyset \\in I \\land \\forall x \\, (x \\in I \\implies x \\cup \\{x\\} \\in I) \\right)$$

Here, $S(x) = x \\cup \\{x\\}$ is the **successor** of $x$.

**Von Neumann ordinals:** Starting from $\\emptyset$:
- $0 = \\emptyset$
- $1 = S(0) = \\{\\emptyset\\}$
- $2 = S(1) = \\{\\emptyset, \\{\\emptyset\\}\\}$
- $3 = S(2) = \\{\\emptyset, \\{\\emptyset\\}, \\{\\emptyset, \\{\\emptyset\\}\\}\\}$
- ...

**Consequence:** This axiom guarantees the existence of infinite sets. The smallest
such set is $\\omega$ (or $\\mathbb{N}$), the set of natural numbers.

**Note:** Without this axiom, all provably existing sets would be finite.""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Naive Set Theory - Paul Halmos, Ch. 11",
        ],
        "prerequisites": ["Axiom of Empty Set", "Axiom of Union", "Axiom of Pairing"],
    },
    {
        "name": "Axiom Schema of Replacement",
        "definition_md": """## Axiom Schema of Replacement

If $F$ is a definable function (expressed by a formula), then for any set $A$,
the image $F[A]$ is also a set:

$$\\forall A \\, \\left( \\forall x \\in A \\, \\exists! y \\, \\varphi(x, y) \\implies \\exists B \\, \\forall y \\, (y \\in B \\iff \\exists x \\in A \\, \\varphi(x, y)) \\right)$$

**Informal:** The image of a set under a definable function is a set.

**Why "Schema":** Like Specification, this is an axiom schema - one axiom for each
formula $\\varphi$ defining a function.

**Power:** This axiom is essential for:
- Constructing ordinals beyond $\\omega$ (transfinite recursion)
- Proving the existence of $V_{\\omega + \\omega}$ and higher stages
- Many advanced set-theoretic constructions

**Note:** Replacement implies Specification (given the other axioms).""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Elements of Set Theory - Herbert Enderton, Ch. 7",
        ],
        "prerequisites": ["Axiom of Extensionality"],
    },
    {
        "name": "Axiom of Regularity",
        "definition_md": """## Axiom of Regularity (Foundation)

Every non-empty set $A$ contains an element disjoint from $A$:

$$\\forall A \\, \\left( A \\neq \\emptyset \\implies \\exists x \\in A \\, (x \\cap A = \\emptyset) \\right)$$

**Consequences:**
1. **No set is a member of itself:** $\\forall x \\, (x \\notin x)$
2. **No infinite descending membership chains:** There is no sequence
   $x_0 \\ni x_1 \\ni x_2 \\ni \\cdots$
3. **The set-theoretic universe is well-founded**

**Proof that $x \\notin x$:** Suppose $x \\in x$. Consider $A = \\{x\\}$. By Regularity,
$A$ has an element disjoint from $A$. But the only element is $x$, and
$x \\cap A = x \\cap \\{x\\} = \\{x\\} \\neq \\emptyset$ (since $x \\in x$). Contradiction.

**Note:** This axiom rules out "exotic" sets and ensures all sets can be built
from $\\emptyset$ by iterating the power set and union operations.""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Elements of Set Theory - Herbert Enderton, Ch. 7",
        ],
        "prerequisites": ["Axiom of Extensionality", "Set Intersection"],
    },
    {
        "name": "Axiom of Choice",
        "definition_md": """## Axiom of Choice (AC)

For any collection $\\mathcal{C}$ of non-empty sets, there exists a function
$f: \\mathcal{C} \\to \\bigcup \\mathcal{C}$ such that for every $S \\in \\mathcal{C}$:

$$f(S) \\in S$$

Such a function $f$ is called a **choice function**.

**Formal statement:**
$$\\forall \\mathcal{C} \\, \\left( \\emptyset \\notin \\mathcal{C} \\implies \\exists f \\, \\forall S \\in \\mathcal{C} \\, (f(S) \\in S) \\right)$$

**Equivalent formulations:**
- **Zorn's Lemma:** Every non-empty partially ordered set in which every chain has
  an upper bound contains a maximal element.
- **Well-Ordering Theorem:** Every set can be well-ordered.
- **Every vector space has a basis.**
- **Tychonoff's Theorem:** Any product of compact spaces is compact.

**Controversy:** AC is independent of ZF (Zermelo-Fraenkel without Choice). It implies
non-constructive existence results like non-measurable sets (Vitali sets).""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 2",
            "Naive Set Theory - Paul Halmos, Ch. 15",
            "The Axiom of Choice - Thomas Jech",
        ],
        "prerequisites": ["Function", "Axiom of Union"],
    },
    # ==========================================================================
    # FUNDAMENTAL SET THEORY CONCEPTS - Level 1
    # ==========================================================================
    {
        "name": "Subset",
        "definition_md": """## Subset

A set $A$ is a **subset** of a set $B$, written $A \\subseteq B$, if every element
of $A$ is also an element of $B$:

$$A \\subseteq B \\iff \\forall x \\, (x \\in A \\implies x \\in B)$$

**Proper subset:** $A \\subsetneq B$ (or $A \\subset B$) means $A \\subseteq B$ and $A \\neq B$.

**Properties:**
- $\\emptyset \\subseteq A$ for any set $A$ (vacuously true)
- $A \\subseteq A$ for any set $A$ (reflexivity)
- If $A \\subseteq B$ and $B \\subseteq A$, then $A = B$ (antisymmetry)
- If $A \\subseteq B$ and $B \\subseteq C$, then $A \\subseteq C$ (transitivity)

**Connection to equality:** By Extensionality:
$$A = B \\iff (A \\subseteq B \\land B \\subseteq A)$$""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Naive Set Theory - Paul Halmos, Ch. 1",
            "Elements of Set Theory - Herbert Enderton, Ch. 1",
        ],
        "prerequisites": ["Axiom of Extensionality"],
    },
    {
        "name": "Set Intersection",
        "definition_md": """## Set Intersection

The **intersection** of sets $A$ and $B$ is the set of elements belonging to both:

$$A \\cap B = \\{x : x \\in A \\land x \\in B\\}$$

**Generalized intersection:** For a non-empty family $\\mathcal{F}$ of sets:
$$\\bigcap \\mathcal{F} = \\{x : \\forall A \\in \\mathcal{F} \\, (x \\in A)\\}$$

**Properties:**
- $A \\cap B = B \\cap A$ (commutativity)
- $(A \\cap B) \\cap C = A \\cap (B \\cap C)$ (associativity)
- $A \\cap A = A$ (idempotence)
- $A \\cap \\emptyset = \\emptyset$
- $A \\cap B \\subseteq A$ and $A \\cap B \\subseteq B$

**Existence:** Given sets $A$ and $B$, the intersection exists by the Axiom Schema
of Specification: $A \\cap B = \\{x \\in A : x \\in B\\}$.

**Note:** $\\bigcap \\emptyset$ is typically undefined or taken to be the universal
class (which is not a set in ZFC).""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Naive Set Theory - Paul Halmos, Ch. 4",
            "Elements of Set Theory - Herbert Enderton, Ch. 2",
        ],
        "prerequisites": ["Axiom Schema of Specification"],
    },
    {
        "name": "Set Difference",
        "definition_md": """## Set Difference

The **set difference** (or **relative complement**) of $B$ in $A$ is:

$$A \\setminus B = \\{x : x \\in A \\land x \\notin B\\}$$

Also written $A - B$.

**Properties:**
- $A \\setminus \\emptyset = A$
- $A \\setminus A = \\emptyset$
- $A \\setminus B \\subseteq A$
- $(A \\setminus B) \\cap B = \\emptyset$
- $A = (A \\cap B) \\cup (A \\setminus B)$ (partition)

**Symmetric difference:**
$$A \\triangle B = (A \\setminus B) \\cup (B \\setminus A) = (A \\cup B) \\setminus (A \\cap B)$$

**Existence:** By Specification: $A \\setminus B = \\{x \\in A : x \\notin B\\}$.""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Naive Set Theory - Paul Halmos, Ch. 4",
            "Elements of Set Theory - Herbert Enderton, Ch. 2",
        ],
        "prerequisites": ["Axiom Schema of Specification"],
    },
    {
        "name": "Ordered Pair",
        "definition_md": """## Ordered Pair

The **ordered pair** $(a, b)$ is defined (Kuratowski definition) as:

$$(a, b) := \\{\\{a\\}, \\{a, b\\}\\}$$

**Characteristic property:** The fundamental property distinguishing ordered pairs
from unordered pairs is:

$$(a, b) = (c, d) \\iff a = c \\land b = d$$

**Proof of characteristic property:**
If $(a, b) = (c, d)$, then $\\{\\{a\\}, \\{a, b\\}\\} = \\{\\{c\\}, \\{c, d\\}\\}$.
- Case 1: If $a = b$, then $(a, b) = \\{\\{a\\}\\}$, so $\\{\\{c\\}, \\{c, d\\}\\} = \\{\\{a\\}\\}$,
  implying $c = d = a = b$.
- Case 2: If $a \\neq b$, then $\\{a\\} \\neq \\{a, b\\}$, and careful case analysis
  yields $a = c$ and $b = d$.

**Alternative definitions:**
- Wiener: $(a, b) = \\{\\{\\{a\\}, \\emptyset\\}, \\{\\{b\\}\\}\\}$
- Short: $(a, b) = \\{a, \\{a, b\\}\\}$ (requires regularity)""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Naive Set Theory - Paul Halmos, Ch. 6",
        ],
        "prerequisites": ["Axiom of Pairing"],
    },
    {
        "name": "Cartesian Product",
        "definition_md": """## Cartesian Product

The **Cartesian product** of sets $A$ and $B$ is the set of all ordered pairs $(a, b)$
where $a \\in A$ and $b \\in B$:

$$A \\times B = \\{(a, b) : a \\in A \\land b \\in B\\}$$

**Properties:**
- $A \\times \\emptyset = \\emptyset \\times A = \\emptyset$
- $A \\times (B \\cup C) = (A \\times B) \\cup (A \\times C)$ (distributivity)
- $A \\times (B \\cap C) = (A \\times B) \\cap (A \\times C)$
- $|A \\times B| = |A| \\cdot |B|$ for finite sets

**Existence in ZFC:** Using Specification and Power Set:
$$A \\times B \\subseteq \\mathcal{P}(\\mathcal{P}(A \\cup B))$$

**Generalization:** For $n$ sets: $A_1 \\times \\cdots \\times A_n$, and for
infinite products $\\prod_{i \\in I} A_i$ (requires Choice for non-empty product).

**Example:** $\\{1, 2\\} \\times \\{a, b\\} = \\{(1, a), (1, b), (2, a), (2, b)\\}$""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Naive Set Theory - Paul Halmos, Ch. 6",
            "Elements of Set Theory - Herbert Enderton, Ch. 3",
        ],
        "prerequisites": ["Ordered Pair", "Axiom of Power Set"],
    },
    {
        "name": "Relation",
        "definition_md": """## Relation

A **relation** from set $A$ to set $B$ is a subset $R \\subseteq A \\times B$.

If $(a, b) \\in R$, we write $a \\mathrel{R} b$ (read "$a$ is related to $b$").

**Domain and range:**
- $\\text{dom}(R) = \\{a : \\exists b \\, ((a, b) \\in R)\\}$
- $\\text{ran}(R) = \\{b : \\exists a \\, ((a, b) \\in R)\\}$

**Special types (for $R \\subseteq A \\times A$):**
- **Reflexive:** $\\forall a \\in A \\, (a \\mathrel{R} a)$
- **Symmetric:** $a \\mathrel{R} b \\implies b \\mathrel{R} a$
- **Antisymmetric:** $a \\mathrel{R} b \\land b \\mathrel{R} a \\implies a = b$
- **Transitive:** $a \\mathrel{R} b \\land b \\mathrel{R} c \\implies a \\mathrel{R} c$

**Equivalence relation:** Reflexive, symmetric, and transitive.
**Partial order:** Reflexive, antisymmetric, and transitive.

**Inverse relation:** $R^{-1} = \\{(b, a) : (a, b) \\in R\\}$""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Naive Set Theory - Paul Halmos, Ch. 7",
            "Elements of Set Theory - Herbert Enderton, Ch. 3",
        ],
        "prerequisites": ["Cartesian Product", "Subset"],
    },
    {
        "name": "Function",
        "definition_md": """## Function

A **function** $f$ from $A$ to $B$, written $f: A \\to B$, is a relation
$f \\subseteq A \\times B$ such that:

1. $\\text{dom}(f) = A$ (total)
2. $\\forall a \\in A \\, \\forall b_1, b_2 \\, ((a, b_1) \\in f \\land (a, b_2) \\in f \\implies b_1 = b_2)$ (single-valued)

**Notation:** If $(a, b) \\in f$, write $f(a) = b$ or $a \\mapsto b$.

**Terminology:**
- $A$ is the **domain**
- $B$ is the **codomain**
- $f[A] = \\{f(a) : a \\in A\\} \\subseteq B$ is the **image** (or range)

**Types:**
- **Injective (one-to-one):** $f(a_1) = f(a_2) \\implies a_1 = a_2$
- **Surjective (onto):** $f[A] = B$
- **Bijective:** Both injective and surjective

**Composition:** $(g \\circ f)(x) = g(f(x))$ for $f: A \\to B$, $g: B \\to C$.""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Naive Set Theory - Paul Halmos, Ch. 8",
            "Elements of Set Theory - Herbert Enderton, Ch. 3",
        ],
        "prerequisites": ["Relation", "Cartesian Product"],
    },
    # ==========================================================================
    # ORDINALS AND CARDINALS - Level 2
    # ==========================================================================
    {
        "name": "Ordinal Number",
        "definition_md": """## Ordinal Number

A set $\\alpha$ is an **ordinal number** (or **ordinal**) if:

1. $\\alpha$ is **transitive:** $\\forall x \\in \\alpha \\, (x \\subseteq \\alpha)$
2. $\\alpha$ is **well-ordered** by $\\in$: every non-empty subset has a least element

**Von Neumann ordinals:** Ordinals are constructed as:
- $0 = \\emptyset$
- $\\alpha + 1 = \\alpha \\cup \\{\\alpha\\}$ (successor)
- $\\lambda = \\bigcup_{\\beta < \\lambda} \\beta$ (limit ordinal)

**Examples:**
- Finite ordinals: $0, 1, 2, 3, \\ldots$ (natural numbers)
- $\\omega = \\{0, 1, 2, \\ldots\\}$ (first infinite ordinal)
- $\\omega + 1 = \\{0, 1, 2, \\ldots, \\omega\\}$

**Properties:**
- Every element of an ordinal is an ordinal
- Ordinals are comparable: $\\alpha \\in \\beta$, $\\alpha = \\beta$, or $\\beta \\in \\alpha$
- **Trichotomy:** $\\alpha < \\beta \\iff \\alpha \\in \\beta$""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 2,
        "is_axiom": False,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Naive Set Theory - Paul Halmos, Ch. 18",
            "Elements of Set Theory - Herbert Enderton, Ch. 7",
        ],
        "prerequisites": ["Axiom of Infinity", "Well-Ordering"],
    },
    {
        "name": "Well-Ordering",
        "definition_md": """## Well-Ordering

A **well-ordering** on a set $A$ is a total order $\\leq$ such that every non-empty
subset of $A$ has a least element:

$$\\forall S \\subseteq A \\, (S \\neq \\emptyset \\implies \\exists m \\in S \\, \\forall x \\in S \\, (m \\leq x))$$

**Equivalently:** A well-ordering is a total order with no infinite descending chains.

**Properties:**
- Every well-ordered set is totally ordered
- Every subset of a well-ordered set is well-ordered
- $\\mathbb{N}$ with the usual $\\leq$ is well-ordered
- $\\mathbb{Z}$ and $\\mathbb{R}$ with usual $\\leq$ are NOT well-ordered

**Well-Ordering Theorem (AC):** Every set can be well-ordered.

**Transfinite induction:** If $P(0)$ holds, and $P(\\alpha)$ for all $\\alpha < \\beta$
implies $P(\\beta)$, then $P(\\alpha)$ holds for all ordinals $\\alpha$.""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 2,
        "is_axiom": False,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Naive Set Theory - Paul Halmos, Ch. 17",
        ],
        "prerequisites": ["Relation", "Axiom of Choice"],
    },
    {
        "name": "Cardinal Number",
        "definition_md": """## Cardinal Number

A **cardinal number** (or **cardinal**) is an ordinal $\\kappa$ that is not
equinumerous with any smaller ordinal:

$$\\kappa \\text{ is a cardinal} \\iff \\forall \\alpha < \\kappa \\, (|\\alpha| \\neq |\\kappa|)$$

**Cardinality:** Two sets have the same **cardinality**, written $|A| = |B|$, if
there exists a bijection $f: A \\to B$.

**Finite cardinals:** $0, 1, 2, 3, \\ldots$ (same as finite ordinals)

**Infinite cardinals (alephs):**
- $\\aleph_0 = |\\mathbb{N}| = \\omega$ (smallest infinite cardinal)
- $\\aleph_1$ = smallest uncountable cardinal
- $\\aleph_\\alpha$ = the $\\alpha$-th infinite cardinal

**Cantor's Theorem:** $|A| < |\\mathcal{P}(A)|$ for all sets $A$.

**Continuum Hypothesis (CH):** $|\\mathbb{R}| = 2^{\\aleph_0} = \\aleph_1$
(independent of ZFC)""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 2,
        "is_axiom": False,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Naive Set Theory - Paul Halmos, Ch. 22-24",
            "Elements of Set Theory - Herbert Enderton, Ch. 6",
        ],
        "prerequisites": ["Ordinal Number", "Function"],
    },
    {
        "name": "Natural Numbers",
        "definition_md": """## Natural Numbers

The **natural numbers** $\\mathbb{N}$ (or $\\omega$) are defined as the smallest
inductive set, i.e., the intersection of all inductive sets:

$$\\mathbb{N} = \\bigcap \\{I : I \\text{ is inductive}\\}$$

where a set $I$ is **inductive** if $\\emptyset \\in I$ and $n \\in I \\implies S(n) \\in I$.

**Von Neumann construction:**
- $0 = \\emptyset$
- $1 = \\{0\\} = \\{\\emptyset\\}$
- $2 = \\{0, 1\\} = \\{\\emptyset, \\{\\emptyset\\}\\}$
- $n + 1 = n \\cup \\{n\\}$

**Peano axioms** (satisfied by $\\mathbb{N}$):
1. $0 \\in \\mathbb{N}$
2. $n \\in \\mathbb{N} \\implies S(n) \\in \\mathbb{N}$
3. $\\forall n \\, (S(n) \\neq 0)$
4. $S(m) = S(n) \\implies m = n$
5. **Induction:** If $P(0)$ and $\\forall n (P(n) \\implies P(S(n)))$, then $\\forall n \\, P(n)$

**Note:** $n \\in \\mathbb{N}$ implies $n = \\{0, 1, \\ldots, n-1\\}$, so $|n| = n$.""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 2,
        "is_axiom": False,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Naive Set Theory - Paul Halmos, Ch. 11",
            "Elements of Set Theory - Herbert Enderton, Ch. 4",
        ],
        "prerequisites": ["Axiom of Infinity", "Set Intersection"],
    },
    {
        "name": "Transfinite Induction",
        "definition_md": """## Transfinite Induction

**Transfinite induction** is a proof technique for well-ordered sets (particularly ordinals).

**Principle:** For a property $P$ and ordinals:

If for every ordinal $\\alpha$:
$$\\left( \\forall \\beta < \\alpha \\, P(\\beta) \\right) \\implies P(\\alpha)$$

Then $P(\\alpha)$ holds for all ordinals.

**Three-case form:** To prove $P(\\alpha)$ for all ordinals:
1. **Base case:** Prove $P(0)$
2. **Successor case:** Prove $P(\\alpha) \\implies P(\\alpha + 1)$
3. **Limit case:** For limit ordinals $\\lambda$, prove
   $\\left( \\forall \\beta < \\lambda \\, P(\\beta) \\right) \\implies P(\\lambda)$

**Transfinite recursion:** Define $F(\\alpha)$ for all ordinals by:
- $F(0) = a$ (base value)
- $F(\\alpha + 1) = G(F(\\alpha))$ (successor rule)
- $F(\\lambda) = H(\\langle F(\\beta) : \\beta < \\lambda \\rangle)$ (limit rule)

**Justification:** Requires the Axiom of Replacement to show the recursion
defines a function on all ordinals.""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 2,
        "is_axiom": False,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Elements of Set Theory - Herbert Enderton, Ch. 7",
        ],
        "prerequisites": ["Ordinal Number", "Well-Ordering", "Axiom Schema of Replacement"],
    },
    # ==========================================================================
    # ADDITIONAL FOUNDATIONAL CONCEPTS - Various Levels
    # ==========================================================================
    {
        "name": "Equivalence Relation",
        "definition_md": """## Equivalence Relation

An **equivalence relation** on a set $A$ is a relation $\\sim \\subseteq A \\times A$
satisfying:

1. **Reflexivity:** $\\forall a \\in A \\, (a \\sim a)$
2. **Symmetry:** $\\forall a, b \\in A \\, (a \\sim b \\implies b \\sim a)$
3. **Transitivity:** $\\forall a, b, c \\in A \\, (a \\sim b \\land b \\sim c \\implies a \\sim c)$

**Equivalence class:** For $a \\in A$, the equivalence class of $a$ is:
$$[a] = \\{x \\in A : x \\sim a\\}$$

**Quotient set:** The set of all equivalence classes:
$$A / {\\sim} = \\{[a] : a \\in A\\}$$

**Partition:** An equivalence relation on $A$ induces a partition of $A$, and
conversely, every partition induces an equivalence relation.

**Examples:**
- Equality ($=$) on any set
- Congruence modulo $n$ on $\\mathbb{Z}$: $a \\equiv b \\pmod{n} \\iff n | (a - b)$
- Same cardinality on sets: $A \\sim B \\iff |A| = |B|$""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Naive Set Theory - Paul Halmos, Ch. 7",
            "Elements of Set Theory - Herbert Enderton, Ch. 3",
        ],
        "prerequisites": ["Relation"],
    },
    {
        "name": "Partial Order",
        "definition_md": """## Partial Order

A **partial order** (or **partial ordering**) on a set $P$ is a relation
$\\leq \\subseteq P \\times P$ satisfying:

1. **Reflexivity:** $\\forall a \\in P \\, (a \\leq a)$
2. **Antisymmetry:** $\\forall a, b \\in P \\, (a \\leq b \\land b \\leq a \\implies a = b)$
3. **Transitivity:** $\\forall a, b, c \\in P \\, (a \\leq b \\land b \\leq c \\implies a \\leq c)$

A set with a partial order is called a **partially ordered set** (or **poset**).

**Strict order:** $a < b \\iff a \\leq b \\land a \\neq b$

**Total order:** A partial order where $\\forall a, b \\, (a \\leq b \\lor b \\leq a)$.

**Examples:**
- $(\\mathbb{N}, \\leq)$ - total order
- $(\\mathcal{P}(X), \\subseteq)$ - partial order (not total if $|X| \\geq 2$)
- $(\\mathbb{N}, |)$ where $a | b$ means "$a$ divides $b$" - partial order

**Special elements:**
- **Minimal:** $a$ is minimal if $b \\leq a \\implies b = a$
- **Maximal:** $a$ is maximal if $a \\leq b \\implies a = b$""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Introduction to Lattices and Order - Davey & Priestley, Ch. 1",
        ],
        "prerequisites": ["Relation"],
    },
    {
        "name": "Zorn's Lemma",
        "definition_md": """## Zorn's Lemma

Let $(P, \\leq)$ be a non-empty partially ordered set. If every **chain**
(totally ordered subset) in $P$ has an **upper bound** in $P$, then $P$
contains at least one **maximal element**.

**Formal statement:**
$$\\left( \\forall C \\subseteq P \\, (C \\text{ is a chain} \\implies \\exists u \\in P \\, \\forall c \\in C \\, (c \\leq u)) \\right) \\implies \\exists m \\in P \\, \\forall x \\in P \\, (m \\leq x \\implies m = x)$$

**Equivalence:** Zorn's Lemma is equivalent to:
- Axiom of Choice
- Well-Ordering Theorem
- Hausdorff Maximal Principle

**Applications:**
- Every vector space has a basis
- Every ring with unity has a maximal ideal
- Every field has an algebraic closure
- Hahn-Banach theorem (functional analysis)

**Warning:** Zorn's Lemma guarantees existence but not uniqueness of maximal elements.""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 2,
        "is_axiom": False,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 2",
            "Naive Set Theory - Paul Halmos, Ch. 16",
            "The Axiom of Choice - Thomas Jech, Ch. 1",
        ],
        "prerequisites": ["Partial Order", "Axiom of Choice"],
    },
    {
        "name": "Countable Set",
        "definition_md": """## Countable Set

A set $A$ is **countable** if there exists an injection $f: A \\to \\mathbb{N}$.

Equivalently:
- $A$ is finite, or
- There exists a bijection $f: A \\to \\mathbb{N}$ ($A$ is **countably infinite**)

**Notation:** $|A| \\leq \\aleph_0$ (countable), $|A| = \\aleph_0$ (countably infinite)

**Properties:**
- Every subset of a countable set is countable
- A countable union of countable sets is countable (requires AC)
- $\\mathbb{Z}$ and $\\mathbb{Q}$ are countable
- Finite products of countable sets are countable

**Cantor's Diagonal Argument:** $\\mathbb{R}$ is **uncountable** ($|\\mathbb{R}| > \\aleph_0$).

**Cantor's Theorem:** For any set $A$, $|\\mathcal{P}(A)| > |A|$, so $\\mathcal{P}(\\mathbb{N})$
is uncountable.

**Example bijection $f: \\mathbb{Z} \\to \\mathbb{N}$:**
$$f(n) = \\begin{cases} 2n & \\text{if } n \\geq 0 \\\\ -2n - 1 & \\text{if } n < 0 \\end{cases}$$""",
        "domain": "MATH",
        "subfield": "set_theory",
        "complexity_level": 2,
        "is_axiom": False,
        "books": [
            "Set Theory - Kenneth Kunen, Ch. 1",
            "Naive Set Theory - Paul Halmos, Ch. 13",
            "Elements of Set Theory - Herbert Enderton, Ch. 6",
        ],
        "prerequisites": ["Cardinal Number", "Natural Numbers", "Function"],
    },
]
