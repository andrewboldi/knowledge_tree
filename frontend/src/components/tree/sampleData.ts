import type { GraphData, Concept } from './types';

const sampleConcepts: Concept[] = [
  {
    id: 'math-set-extensionality',
    name: 'Axiom of Extensionality',
    definition_md: `## Axiom of Extensionality

Two sets are equal if and only if they contain the same elements:

$$\\forall A \\forall B \\left( \\forall x (x \\in A \\iff x \\in B) \\implies A = B \\right)$$

**Informal:** Sets are determined entirely by their members.`,
    domain: 'MATH',
    subfield: 'set_theory',
    complexity_level: 0,
    is_axiom: true,
    is_verified: true,
    books: ['Set Theory - Kunen, Ch. 1', 'Naive Set Theory - Halmos'],
    llm_summary: 'Two sets are equal iff they have the same elements.',
  },
  {
    id: 'math-set-empty',
    name: 'Empty Set',
    definition_md: `## Empty Set

The **empty set**, denoted $\\emptyset$, is the unique set with no elements.`,
    domain: 'MATH',
    subfield: 'set_theory',
    complexity_level: 0,
    is_axiom: true,
    is_verified: true,
    llm_summary: 'The unique set containing no elements.',
  },
  {
    id: 'math-set-ordered-pair',
    name: 'Ordered Pair',
    definition_md: `## Ordered Pair

$(a, b) := \\{\\{a\\}, \\{a, b\\}\\}$`,
    domain: 'MATH',
    subfield: 'set_theory',
    complexity_level: 1,
    is_axiom: false,
    is_verified: true,
    llm_summary: 'A pair where order matters: (a,b) ≠ (b,a).',
  },
  {
    id: 'math-linalg-vectorspace',
    name: 'Vector Space',
    definition_md: `## Vector Space

A vector space over a field $F$ is a set $V$ with addition and scalar multiplication.`,
    domain: 'MATH',
    subfield: 'linear_algebra',
    complexity_level: 2,
    is_axiom: false,
    is_verified: true,
    llm_summary: 'Set with vector addition and scalar multiplication.',
  },
  {
    id: 'physics-mechanics-newton2',
    name: "Newton's Second Law",
    definition_md: `## Newton's Second Law

$$\\mathbf{F} = m\\mathbf{a}$$`,
    domain: 'PHYSICS',
    subfield: 'mechanics',
    complexity_level: 0,
    is_axiom: true,
    is_verified: true,
    llm_summary: 'Force equals mass times acceleration.',
  },
  {
    id: 'physics-em-maxwell',
    name: "Maxwell's Equations",
    definition_md: `## Maxwell's Equations

The four fundamental equations of electromagnetism.`,
    domain: 'PHYSICS',
    subfield: 'electromagnetism',
    complexity_level: 2,
    is_axiom: false,
    is_verified: true,
    llm_summary: 'Four equations describing electromagnetic fields.',
  },
  {
    id: 'cs-complexity-bigO',
    name: 'Big-O Notation',
    definition_md: `## Big-O Notation

$f(n) = O(g(n))$ if $f$ grows no faster than $g$ asymptotically.`,
    domain: 'CS',
    subfield: 'complexity',
    complexity_level: 1,
    is_axiom: false,
    is_verified: true,
    llm_summary: 'Describes upper bound on algorithm growth rate.',
  },
  {
    id: 'chem-thermo-gibbs',
    name: 'Gibbs Free Energy',
    definition_md: `## Gibbs Free Energy

$G = H - TS$`,
    domain: 'CHEMISTRY',
    subfield: 'thermodynamics',
    complexity_level: 1,
    is_axiom: false,
    is_verified: true,
    llm_summary: 'Predicts spontaneity of chemical reactions.',
  },
  {
    id: 'bio-genetics-codon',
    name: 'Codon',
    definition_md: `## Codon

A triplet of nucleotides in mRNA specifying an amino acid.`,
    domain: 'BIOLOGY',
    subfield: 'genetics',
    complexity_level: 1,
    is_axiom: false,
    is_verified: true,
    llm_summary: 'Three-nucleotide sequence encoding one amino acid.',
  },
];

export const sampleGraphData: GraphData = {
  nodes: sampleConcepts.map((c) => ({
    id: c.id,
    name: c.name,
    domain: c.domain,
    complexity_level: c.complexity_level,
    is_axiom: c.is_axiom,
    _concept: c,
  })),
  links: [
    { source: 'math-set-extensionality', target: 'math-set-empty' },
    { source: 'math-set-empty', target: 'math-set-ordered-pair' },
    { source: 'math-set-ordered-pair', target: 'math-linalg-vectorspace' },
    { source: 'physics-mechanics-newton2', target: 'physics-em-maxwell' },
    { source: 'math-linalg-vectorspace', target: 'physics-em-maxwell' },
    { source: 'chem-thermo-gibbs', target: 'bio-genetics-codon' },
  ],
};
