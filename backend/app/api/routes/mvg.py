"""MVG (Minimum Viable Graph) API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ...services.mvg_service import get_mvg_service, MVGResult


router = APIRouter(prefix="/mvg", tags=["mvg"])


class MVGRequest(BaseModel):
    """Request to generate a minimum viable graph."""

    target: str = Field(..., description="Target concept to learn")
    domain: str = Field(
        default="MATH",
        description="Knowledge domain (MATH, PHYSICS, CHEMISTRY, BIOLOGY, CS)",
    )


class MVGNodeResponse(BaseModel):
    """A node in the learning path."""

    name: str
    description: str
    is_axiom: bool
    concept_id: str | None = None


class MVGResponse(BaseModel):
    """Response containing the minimum viable graph."""

    target: str
    domain: str
    path: list[MVGNodeResponse]
    explanation: str

    @classmethod
    def from_result(cls, result: MVGResult) -> "MVGResponse":
        return cls(
            target=result.target,
            domain=result.domain,
            path=[
                MVGNodeResponse(
                    name=node.name,
                    description=node.description,
                    is_axiom=node.is_axiom,
                    concept_id=node.concept_id,
                )
                for node in result.path
            ],
            explanation=result.explanation,
        )


@router.post("/generate", response_model=MVGResponse)
async def generate_mvg(request: MVGRequest) -> MVGResponse:
    """Generate a minimum viable graph for learning a target concept.

    Returns the minimal prerequisite path from axioms to the target concept.
    """
    service = get_mvg_service()
    try:
        result = await service.generate(target=request.target, domain=request.domain)
        return MVGResponse.from_result(result)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=f"LLM service error: {e}")
