#!/usr/bin/env python3
"""Initialize the Neo4j database schema."""

import sys
import time

sys.path.insert(0, str(__file__).rsplit("/", 2)[0])

from app.db.neo4j_client import Neo4jClient


def wait_for_neo4j(client: Neo4jClient, max_retries: int = 30, delay: float = 2.0):
    """Wait for Neo4j to be available."""
    for i in range(max_retries):
        try:
            client.connect()
            client.execute_query("RETURN 1")
            print("Neo4j is available.")
            return True
        except Exception as e:
            if i < max_retries - 1:
                print(f"Waiting for Neo4j... ({i + 1}/{max_retries})")
                time.sleep(delay)
            else:
                print(f"Failed to connect to Neo4j: {e}")
                return False
    return False


def main():
    """Initialize the database schema."""
    print("Initializing Knowledge Tree Neo4j schema...")

    client = Neo4jClient()

    if not wait_for_neo4j(client):
        sys.exit(1)

    print("Creating schema constraints and indexes...")
    client.init_schema()
    print("Schema initialization complete.")

    # Verify schema was created
    result = client.execute_query("SHOW CONSTRAINTS")
    print(f"Constraints: {len(result)}")

    result = client.execute_query("SHOW INDEXES")
    print(f"Indexes: {len(result)}")

    client.close()
    print("Done.")


if __name__ == "__main__":
    main()
