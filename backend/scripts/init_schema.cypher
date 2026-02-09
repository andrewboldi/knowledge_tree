// Knowledge Tree Neo4j Schema Initialization
// Run this script to set up the Concept node schema and REQUIRES relationship

// Create constraints for unique IDs
CREATE CONSTRAINT concept_id_unique IF NOT EXISTS
FOR (c:Concept) REQUIRE c.id IS UNIQUE;

// Create index on frequently queried fields
CREATE INDEX concept_name_index IF NOT EXISTS
FOR (c:Concept) ON (c.name);

CREATE INDEX concept_domain_index IF NOT EXISTS
FOR (c:Concept) ON (c.domain);

CREATE INDEX concept_subfield_index IF NOT EXISTS
FOR (c:Concept) ON (c.subfield);

CREATE INDEX concept_complexity_index IF NOT EXISTS
FOR (c:Concept) ON (c.complexity_level);

CREATE INDEX concept_axiom_index IF NOT EXISTS
FOR (c:Concept) ON (c.is_axiom);

// Example Concept node structure (documentation)
// (:Concept {
//   id: String,                     // UUID - unique identifier
//   name: String,                   // "Vector Space", "Derivative", "Eigenvalue"
//
//   // DEFINITION IN MARKDOWN + LATEX
//   definition_md: String,          // Full markdown definition with LaTeX
//
//   domain: String,                 // MATH, PHYSICS, CHEMISTRY, BIOLOGY, CS
//   subfield: String,               // "linear_algebra", "analysis", "mechanics"
//   complexity_level: Integer,      // 0 = axiom, higher = more complex
//
//   // Resources (stored as JSON arrays in Neo4j)
//   books: [String],                // ["Linear Algebra Done Right - Axler, Ch. 1"]
//   papers: [String],               // ["arXiv:1234.5678", "DOI:10.1000/xyz"]
//   articles: [String],             // URLs
//
//   // Related (non-prerequisite connections)
//   related_concepts: [String],     // IDs of related concepts
//
//   // LLM-readable format
//   llm_summary: String,            // Compact version for LLM context
//
//   is_axiom: Boolean,
//   is_verified: Boolean
// })

// REQUIRES relationship represents prerequisites
// (concept_a:Concept)-[:REQUIRES]->(concept_b:Concept)
// Meaning: To understand concept_a, you must first understand concept_b
