"""Neo4j database client for Knowledge Tree."""

import os
from neo4j import GraphDatabase
from typing import Optional


class Neo4jClient:
    """Client for Neo4j database operations."""

    def __init__(
        self,
        uri: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "knowledge_tree_dev")
        self._driver = None

    def connect(self):
        """Establish connection to Neo4j."""
        self._driver = GraphDatabase.driver(
            self.uri, auth=(self.user, self.password)
        )

    def close(self):
        """Close the database connection."""
        if self._driver:
            self._driver.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def execute_query(self, query: str, parameters: Optional[dict] = None):
        """Execute a Cypher query and return results."""
        with self._driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def init_schema(self):
        """Initialize the database schema with constraints and indexes."""
        schema_queries = [
            # Unique constraint on Concept.id
            """CREATE CONSTRAINT concept_id_unique IF NOT EXISTS
               FOR (c:Concept) REQUIRE c.id IS UNIQUE""",
            # Indexes for frequently queried fields
            """CREATE INDEX concept_name_index IF NOT EXISTS
               FOR (c:Concept) ON (c.name)""",
            """CREATE INDEX concept_domain_index IF NOT EXISTS
               FOR (c:Concept) ON (c.domain)""",
            """CREATE INDEX concept_subfield_index IF NOT EXISTS
               FOR (c:Concept) ON (c.subfield)""",
            """CREATE INDEX concept_complexity_index IF NOT EXISTS
               FOR (c:Concept) ON (c.complexity_level)""",
            """CREATE INDEX concept_axiom_index IF NOT EXISTS
               FOR (c:Concept) ON (c.is_axiom)""",
        ]
        for query in schema_queries:
            self.execute_query(query)


# Singleton instance
_client: Optional[Neo4jClient] = None


def get_client() -> Neo4jClient:
    """Get or create the Neo4j client singleton."""
    global _client
    if _client is None:
        _client = Neo4jClient()
        _client.connect()
    return _client
