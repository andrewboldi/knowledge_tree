"""User contribution endpoints - requires Firebase authentication."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ...auth.firebase_auth import FirebaseUser, get_current_user
from ...db.concept import Concept, ConceptRepository, generate_concept_id
from ...db.contribution import (
    ContributionRepository,
    create_contribution_from_user,
)


router = APIRouter(prefix="/contributions", tags=["contributions"])


# Request models


class CreateConceptRequest(BaseModel):
    """Request body for creating a new concept."""

    name: str
    definition_md: str  # Markdown + LaTeX definition
    domain: str  # MATH, PHYSICS, CHEMISTRY, BIOLOGY, CS
    subfield: str
    complexity_level: int = 1
    books: list[str] = []
    papers: list[str] = []
    articles: list[str] = []
    related_concepts: list[str] = []
    prerequisite_ids: list[str] = []  # IDs of prerequisite concepts


class AddResourceRequest(BaseModel):
    """Request body for adding a resource to a concept."""

    resource_type: str  # "book", "paper", "article"
    resource: str  # The book/paper/article reference


# Response models


class ConceptContributionResponse(BaseModel):
    """Response after creating a concept contribution."""

    concept_id: str
    contribution_id: str
    message: str


class ResourceContributionResponse(BaseModel):
    """Response after adding a resource to a concept."""

    concept_id: str
    contribution_id: str
    resource_type: str
    message: str


# Repositories
_concept_repo = ConceptRepository()
_contribution_repo = ContributionRepository()


@router.post("/concept", response_model=ConceptContributionResponse)
async def create_concept(
    request: CreateConceptRequest,
    user: FirebaseUser = Depends(get_current_user),
) -> ConceptContributionResponse:
    """Create a new concept definition.

    Requires Firebase authentication. The concept will be stored with user attribution.
    """
    # Validate domain
    valid_domains = {"MATH", "PHYSICS", "CHEMISTRY", "BIOLOGY", "CS"}
    if request.domain not in valid_domains:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid domain. Must be one of: {', '.join(valid_domains)}",
        )

    # Validate complexity level
    if request.complexity_level < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complexity level must be non-negative",
        )

    # Generate concept ID
    concept_id = generate_concept_id(request.domain, request.subfield, request.name)

    # Create the concept
    concept = Concept(
        id=concept_id,
        name=request.name,
        definition_md=request.definition_md,
        domain=request.domain,
        subfield=request.subfield,
        complexity_level=request.complexity_level,
        books=request.books,
        papers=request.papers,
        articles=request.articles,
        related_concepts=request.related_concepts,
        llm_summary="",  # Will be generated later
        is_axiom=request.complexity_level == 0,
        is_verified=False,  # User contributions start unverified
    )

    try:
        _concept_repo.create(concept)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create concept: {str(e)}",
        )

    # Add prerequisite relationships
    for prereq_id in request.prerequisite_ids:
        prereq = _concept_repo.get_by_id(prereq_id)
        if prereq is None:
            # Skip invalid prerequisite IDs but don't fail
            continue
        _concept_repo.add_requires(concept_id, prereq_id)

    # Record the contribution
    contribution = create_contribution_from_user(
        user_id=user.uid,
        concept_id=concept_id,
        contribution_type="concept",
        user_email=user.email,
        user_display_name=user.display_name,
    )
    _contribution_repo.create(contribution)

    return ConceptContributionResponse(
        concept_id=concept_id,
        contribution_id=contribution.id,
        message=f"Successfully created concept '{request.name}'",
    )


@router.post("/{concept_id}/resource", response_model=ResourceContributionResponse)
async def add_resource(
    concept_id: str,
    request: AddResourceRequest,
    user: FirebaseUser = Depends(get_current_user),
) -> ResourceContributionResponse:
    """Add a book, paper, or article to an existing concept.

    Requires Firebase authentication.
    """
    # Validate resource type
    valid_types = {"book", "paper", "article"}
    if request.resource_type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid resource type. Must be one of: {', '.join(valid_types)}",
        )

    # Get the existing concept
    concept = _concept_repo.get_by_id(concept_id)
    if concept is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Concept {concept_id} not found",
        )

    # Add the resource to the appropriate list
    from ...db.neo4j_client import get_client

    client = get_client()

    if request.resource_type == "book":
        # Append to books array
        query = """
        MATCH (c:Concept {id: $concept_id})
        SET c.books = c.books + $resource
        RETURN c
        """
    elif request.resource_type == "paper":
        # Append to papers array
        query = """
        MATCH (c:Concept {id: $concept_id})
        SET c.papers = c.papers + $resource
        RETURN c
        """
    else:  # article
        # Append to articles array
        query = """
        MATCH (c:Concept {id: $concept_id})
        SET c.articles = c.articles + $resource
        RETURN c
        """

    try:
        client.execute_query(query, {"concept_id": concept_id, "resource": request.resource})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add resource: {str(e)}",
        )

    # Record the contribution
    contribution = create_contribution_from_user(
        user_id=user.uid,
        concept_id=concept_id,
        contribution_type=request.resource_type,
        user_email=user.email,
        user_display_name=user.display_name,
    )
    _contribution_repo.create(contribution)

    return ResourceContributionResponse(
        concept_id=concept_id,
        contribution_id=contribution.id,
        resource_type=request.resource_type,
        message=f"Successfully added {request.resource_type} to concept",
    )
