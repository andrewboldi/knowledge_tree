"""Graph API endpoints for Knowledge Tree visualization."""

from fastapi import APIRouter
from pydantic import BaseModel

from ...db.neo4j_client import get_client


router = APIRouter(prefix="/graph", tags=["graph"])


class TreeNode(BaseModel):
    """Node in the knowledge tree."""

    id: str
    name: str
    domain: str
    subfield: str
    complexity_level: int
    is_axiom: bool
    children: list["TreeNode"] = []


class TreeResponse(BaseModel):
    """Tree rooted at axioms for a domain."""

    domain: str
    roots: list[TreeNode]
    total_nodes: int


@router.get("/tree/{domain}", response_model=TreeResponse)
async def get_domain_tree(domain: str) -> TreeResponse:
    """Get the knowledge tree for a domain, rooted at axioms.

    The tree structure follows REQUIRES relationships:
    - Axioms are root nodes (complexity_level = 0)
    - Non-axiom concepts branch downward based on prerequisites
    """
    client = get_client()

    # Get all concepts and their prerequisite relationships for the domain
    query = """
    MATCH (c:Concept {domain: $domain})
    OPTIONAL MATCH (c)-[:REQUIRES]->(p:Concept)
    RETURN c.id AS id,
           c.name AS name,
           c.domain AS domain,
           c.subfield AS subfield,
           c.complexity_level AS complexity_level,
           c.is_axiom AS is_axiom,
           collect(p.id) AS prerequisite_ids
    ORDER BY c.complexity_level
    """
    results = client.execute_query(query, {"domain": domain.upper()})

    # Build lookup maps
    nodes: dict[str, TreeNode] = {}
    parent_map: dict[str, list[str]] = {}  # child_id -> parent_ids

    for row in results:
        node_id = row["id"]
        nodes[node_id] = TreeNode(
            id=node_id,
            name=row["name"],
            domain=row["domain"],
            subfield=row["subfield"],
            complexity_level=row["complexity_level"],
            is_axiom=row["is_axiom"],
            children=[],
        )
        # Track parent relationships (a concept's prerequisites are its parents in the tree)
        prereq_ids = [p for p in row["prerequisite_ids"] if p is not None]
        parent_map[node_id] = prereq_ids

    # Build tree by adding children to parents
    # A concept becomes a child of its prerequisites
    roots: list[TreeNode] = []
    added_as_child: set[str] = set()

    for node_id, prereq_ids in parent_map.items():
        if not prereq_ids:
            # No prerequisites - this is a root (axiom)
            roots.append(nodes[node_id])
        else:
            # Add as child to each prerequisite
            for prereq_id in prereq_ids:
                if prereq_id in nodes:
                    nodes[prereq_id].children.append(nodes[node_id])
                    added_as_child.add(node_id)

    # Also add nodes that have no prerequisites but aren't marked as axioms
    for node_id, node in nodes.items():
        if node_id not in added_as_child and node_id not in [r.id for r in roots]:
            roots.append(node)

    return TreeResponse(
        domain=domain.upper(),
        roots=roots,
        total_nodes=len(nodes),
    )
