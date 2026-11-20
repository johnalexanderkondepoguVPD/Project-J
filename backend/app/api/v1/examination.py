from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status

from app.schemas.examination import (
    ExaminationCreate,
    ExaminationUpdate,
    ExaminationResponse,
    PaginatedExaminationResponse,
    ExamBodySummary,
)
from app.services.examination import ExaminationService
from app.dependencies import get_current_active_user
from app.schemas.user import UserResponse


router = APIRouter(prefix="/exams", tags=["Examination Catalog"])


@router.get(
    "",
    response_model=PaginatedExaminationResponse,
    summary="List examinations",
    description=(
        "List and discover government examinations with keyword search, "
        "faceted filters (conducting body, exam type, level), and pagination."
    ),
)
def list_examinations(
    q: Optional[str] = Query(None, description="Search term in name, abbreviation, or conducting body"),
    conducting_body: Optional[str] = Query(None, description="Filter by conducting organization (e.g. UPSC, SSC)"),
    exam_type: Optional[str] = Query(None, description="Filter by exam type (e.g. UPSC, SSC, Banking, Railways)"),
    level: Optional[str] = Query(None, description="Filter by jurisdiction level (National, State)"),
    is_active: Optional[bool] = Query(True, description="Filter by active status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> PaginatedExaminationResponse:
    """Retrieve paginated examinations matching search and filter parameters."""
    service = ExaminationService()
    return service.list_examinations(
        q=q,
        conducting_body=conducting_body,
        exam_type=exam_type,
        level=level,
        is_active=is_active,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/bodies",
    response_model=List[ExamBodySummary],
    summary="List conducting bodies",
    description="Retrieve aggregated list of all official exam bodies with their active examination counts.",
)
def list_conducting_bodies() -> List[ExamBodySummary]:
    """Retrieve all distinct exam bodies and counts."""
    service = ExaminationService()
    return service.list_conducting_bodies()


@router.get(
    "/{exam_id}",
    response_model=ExaminationResponse,
    summary="Get examination details",
    description="Retrieve full details for a specific examination, including syllabus, eligibility, and exam pattern.",
    responses={
        404: {"description": "Examination not found"},
    },
)
def get_examination(exam_id: int) -> ExaminationResponse:
    """Retrieve examination details by ID."""
    service = ExaminationService()
    return service.get_examination_by_id(exam_id)


@router.post(
    "",
    response_model=ExaminationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create examination",
    description="Add a new examination to the catalog. Requires an authenticated user.",
    responses={
        401: {"description": "Authentication required"},
        422: {"description": "Validation error or duplicate abbreviation"},
    },
)
def create_examination(
    exam_data: ExaminationCreate,
    current_user: UserResponse = Depends(get_current_active_user),
) -> ExaminationResponse:
    """Create a new examination entry."""
    service = ExaminationService()
    return service.create_examination(exam_data)


@router.put(
    "/{exam_id}",
    response_model=ExaminationResponse,
    summary="Update examination",
    description="Update an existing examination definition. Requires an authenticated user.",
    responses={
        401: {"description": "Authentication required"},
        404: {"description": "Examination not found"},
    },
)
def update_examination(
    exam_id: int,
    update_data: ExaminationUpdate,
    current_user: UserResponse = Depends(get_current_active_user),
) -> ExaminationResponse:
    """Update an examination by ID."""
    service = ExaminationService()
    return service.update_examination(exam_id, update_data)


@router.delete(
    "/{exam_id}",
    summary="Deactivate or delete examination",
    description="Deactivate (soft delete) or remove an examination. Requires an authenticated user.",
    responses={
        401: {"description": "Authentication required"},
        404: {"description": "Examination not found"},
    },
)
def delete_examination(
    exam_id: int,
    soft: bool = Query(True, description="Whether to soft-delete (set is_active=False) or hard delete"),
    current_user: UserResponse = Depends(get_current_active_user),
) -> dict:
    """Delete or deactivate an examination by ID."""
    service = ExaminationService()
    return service.delete_examination(exam_id, soft=soft)


@router.post(
    "/seed/initial",
    summary="Seed initial examination catalog",
    description="Seeds verified official examinations (UPSC CSE, SSC CGL, IBPS PO, RRB NTPC, etc.) if the table is empty.",
)
def seed_catalog() -> dict:
    """Seed initial official examinations if not already populated."""
    service = ExaminationService()
    count = service.seed_initial_catalog()
    return {"message": f"Successfully seeded {count} examinations", "seeded": count}
