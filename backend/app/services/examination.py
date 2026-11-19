import math
from typing import Optional, Dict, Any, List
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session

from app.Models.examination import Examination
from app.schemas.examination import (
    ExaminationCreate,
    ExaminationUpdate,
    ExaminationResponse,
    PaginatedExaminationResponse,
    ExamBodySummary,
)
from app.core.exceptions import NotFoundException, ValidationException
from app.database import SessionLocal


# Seed catalog for major Indian government examinations
SEED_EXAMINATIONS = [
    {
        "name": "Civil Services Examination",
        "abbreviation": "UPSC CSE",
        "conducting_body": "Union Public Service Commission",
        "exam_type": "UPSC",
        "level": "National",
        "subject": "General Studies & Optional",
        "frequency": "Annual",
        "eligibility_criteria": "Graduation in any discipline from a recognized university. Age 21-32 years.",
        "exam_pattern": {
            "prelims": {"paper1": "General Studies (200 marks)", "paper2": "CSAT (200 marks, qualifying 33%)"},
            "mains": {"written_papers": 9, "written_marks": 1750, "interview_marks": 275},
            "total_marks": 2025,
            "negative_marking": "1/3rd mark deduction in Prelims",
        },
        "syllabus": "History of India, Indian and World Geography, Indian Polity and Governance, Economic and Social Development, Environmental Ecology, General Science, Current Events.",
        "official_website": "https://upsc.gov.in",
    },
    {
        "name": "Combined Graduate Level Examination",
        "abbreviation": "SSC CGL",
        "conducting_body": "Staff Selection Commission",
        "exam_type": "SSC",
        "level": "National",
        "subject": "General Intelligence, Quantitative Aptitude, English, General Awareness",
        "frequency": "Annual",
        "eligibility_criteria": "Bachelor's degree from a recognized university. Age limit 18-32 years (post-dependent).",
        "exam_pattern": {
            "tier1": {"questions": 100, "marks": 200, "duration_minutes": 60, "negative_marking": "0.50 marks"},
            "tier2": {"sections": ["Mathematical Abilities", "Reasoning", "English", "General Awareness", "Computer Knowledge"]},
        },
        "syllabus": "General Intelligence & Reasoning, General Awareness, Quantitative Aptitude, English Comprehension, Computer Proficiency.",
        "official_website": "https://ssc.gov.in",
    },
    {
        "name": "Probationary Officers / Management Trainees",
        "abbreviation": "IBPS PO",
        "conducting_body": "Institute of Banking Personnel Selection",
        "exam_type": "Banking",
        "level": "National",
        "subject": "Quantitative Aptitude, Reasoning Ability, English Language, General & Banking Awareness",
        "frequency": "Annual",
        "eligibility_criteria": "Graduation in any discipline. Age limit 20-30 years.",
        "exam_pattern": {
            "prelims": {"questions": 100, "marks": 100, "duration_minutes": 60, "negative_marking": "0.25 marks"},
            "mains": {"objective_marks": 200, "descriptive_marks": 25, "interview_marks": 100},
        },
        "syllabus": "Data Analysis & Interpretation, Reasoning & Computer Aptitude, General/Economy/Banking Awareness, English Language.",
        "official_website": "https://ibps.in",
    },
    {
        "name": "Non-Technical Popular Categories",
        "abbreviation": "RRB NTPC",
        "conducting_body": "Railway Recruitment Boards",
        "exam_type": "Railways",
        "level": "National",
        "subject": "General Awareness, Mathematics, General Intelligence and Reasoning",
        "frequency": "Biennial",
        "eligibility_criteria": "12th pass (Undergraduate posts) or Bachelor's Degree (Graduate posts). Age 18-33 years.",
        "exam_pattern": {
            "cbt1": {"questions": 100, "duration_minutes": 90, "negative_marking": "1/3rd mark"},
            "cbt2": {"questions": 120, "duration_minutes": 90, "negative_marking": "1/3rd mark"},
        },
        "syllabus": "Mathematics (Number System, Decimals, Fractions, LCM, HCF, Ratio), General Intelligence & Reasoning, General Awareness (Current Events, Indian History, Art & Culture).",
        "official_website": "https://indianrailways.gov.in",
    },
    {
        "name": "Combined Defence Services Examination",
        "abbreviation": "UPSC CDS",
        "conducting_body": "Union Public Service Commission",
        "exam_type": "UPSC",
        "level": "National",
        "subject": "English, General Knowledge, Elementary Mathematics",
        "frequency": "Biennial",
        "eligibility_criteria": "Degree of a recognized University (IMA/OTA) or Engineering degree (Naval/Air Force). Age 19-24 years.",
        "exam_pattern": {
            "written": {"papers": ["English", "General Knowledge", "Elementary Mathematics"], "marks_each": 100},
            "ssb_interview": {"marks": 300},
        },
        "syllabus": "English vocabulary and grammar, General Knowledge on history, science, geography, Elementary Mathematics up to Class 10.",
        "official_website": "https://upsc.gov.in",
    },
    {
        "name": "National Eligibility cum Entrance Test (Undergraduate)",
        "abbreviation": "NEET UG",
        "conducting_body": "National Testing Agency",
        "exam_type": "NTA",
        "level": "National",
        "subject": "Physics, Chemistry, Biology (Botany & Zoology)",
        "frequency": "Annual",
        "eligibility_criteria": "Passed Class 12 with Physics, Chemistry, Biology/Biotechnology. Minimum 17 years of age.",
        "exam_pattern": {
            "questions": 200,
            "to_attempt": 180,
            "total_marks": 720,
            "duration_minutes": 200,
            "marking_scheme": "+4 for correct, -1 for incorrect",
        },
        "syllabus": "Physics, Chemistry, Botany, and Zoology curriculum of Classes 11 and 12 (NCERT).",
        "official_website": "https://neet.nta.nic.in",
    },
]


class ExaminationService:
    """Business logic and data access for Exam Bodies and Examinations Catalog."""

    def __init__(self, db: Optional[Session] = None):
        self._db = db

    def _get_db(self) -> Session:
        if self._db is not None:
            return self._db
        return SessionLocal()

    def _close_db_if_local(self, db: Session) -> None:
        if self._db is None:
            db.close()

    def list_examinations(
        self,
        q: Optional[str] = None,
        conducting_body: Optional[str] = None,
        exam_type: Optional[str] = None,
        level: Optional[str] = None,
        is_active: Optional[bool] = True,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedExaminationResponse:
        """List examinations with text search, faceted filtering, and pagination."""
        db = self._get_db()
        try:
            # Base query
            query = select(Examination)

            # Text search filter
            if q:
                search_term = f"%{q.strip()}%"
                query = query.where(
                    or_(
                        Examination.name.ilike(search_term),
                        Examination.abbreviation.ilike(search_term),
                        Examination.conducting_body.ilike(search_term),
                        Examination.subject.ilike(search_term),
                    )
                )

            # Faceted filters
            if conducting_body:
                query = query.where(Examination.conducting_body == conducting_body)
            if exam_type:
                query = query.where(Examination.exam_type == exam_type)
            if level:
                query = query.where(Examination.level == level)
            if is_active is not None:
                query = query.where(Examination.is_active == is_active)

            # Count total matching records
            count_query = select(func.count()).select_from(query.subquery())
            total = db.execute(count_query).scalar_one()

            # Pagination
            page = max(1, page)
            page_size = max(1, min(page_size, 100))
            offset = (page - 1) * page_size
            total_pages = math.ceil(total / page_size) if total > 0 else 0

            # Execute paginated query ordered by name
            items_query = query.order_by(Examination.name).offset(offset).limit(page_size)
            records = db.execute(items_query).scalars().all()

            return PaginatedExaminationResponse(
                items=[ExaminationResponse.model_validate(r) for r in records],
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages,
            )
        finally:
            self._close_db_if_local(db)

    def get_examination_by_id(self, exam_id: int) -> ExaminationResponse:
        """Fetch single examination by its unique ID."""
        db = self._get_db()
        try:
            stmt = select(Examination).where(Examination.id == exam_id)
            exam = db.execute(stmt).scalar_one_or_none()
            if not exam:
                raise NotFoundException(detail=f"Examination with ID {exam_id} not found")
            return ExaminationResponse.model_validate(exam)
        finally:
            self._close_db_if_local(db)

    def list_conducting_bodies(self) -> List[ExamBodySummary]:
        """Aggregate list of distinct conducting bodies and their exam counts."""
        db = self._get_db()
        try:
            stmt = (
                select(
                    Examination.conducting_body,
                    Examination.exam_type,
                    func.count(Examination.id).label("exam_count"),
                )
                .where(Examination.is_active == True)
                .group_by(Examination.conducting_body, Examination.exam_type)
                .order_by(func.count(Examination.id).desc())
            )
            rows = db.execute(stmt).all()
            return [
                ExamBodySummary(
                    conducting_body=r[0],
                    exam_type=r[1] or "General",
                    exam_count=r[2],
                )
                for r in rows
            ]
        finally:
            self._close_db_if_local(db)

    def create_examination(self, exam_data: ExaminationCreate) -> ExaminationResponse:
        """Create a new examination entry."""
        db = self._get_db()
        try:
            # Check unique abbreviation if supplied
            if exam_data.abbreviation:
                stmt = select(Examination).where(Examination.abbreviation == exam_data.abbreviation)
                if db.execute(stmt).scalar_one_or_none():
                    raise ValidationException(
                        detail=f"Examination with abbreviation '{exam_data.abbreviation}' already exists"
                    )

            exam = Examination(**exam_data.model_dump())
            db.add(exam)
            db.commit()
            db.refresh(exam)
            return ExaminationResponse.model_validate(exam)
        except Exception:
            db.rollback()
            raise
        finally:
            self._close_db_if_local(db)

    def update_examination(self, exam_id: int, update_data: ExaminationUpdate) -> ExaminationResponse:
        """Update an existing examination."""
        db = self._get_db()
        try:
            stmt = select(Examination).where(Examination.id == exam_id)
            exam = db.execute(stmt).scalar_one_or_none()
            if not exam:
                raise NotFoundException(detail=f"Examination with ID {exam_id} not found")

            # Check abbreviation collision if changed
            if update_data.abbreviation and update_data.abbreviation != exam.abbreviation:
                dup_stmt = select(Examination).where(
                    Examination.abbreviation == update_data.abbreviation,
                    Examination.id != exam_id,
                )
                if db.execute(dup_stmt).scalar_one_or_none():
                    raise ValidationException(
                        detail=f"Examination with abbreviation '{update_data.abbreviation}' already exists"
                    )

            # Apply only supplied fields
            for field, val in update_data.model_dump(exclude_unset=True).items():
                setattr(exam, field, val)

            db.commit()
            db.refresh(exam)
            return ExaminationResponse.model_validate(exam)
        except Exception:
            db.rollback()
            raise
        finally:
            self._close_db_if_local(db)

    def delete_examination(self, exam_id: int, soft: bool = True) -> Dict[str, Any]:
        """Delete an examination (soft-delete default)."""
        db = self._get_db()
        try:
            stmt = select(Examination).where(Examination.id == exam_id)
            exam = db.execute(stmt).scalar_one_or_none()
            if not exam:
                raise NotFoundException(detail=f"Examination with ID {exam_id} not found")

            if soft:
                exam.is_active = False
                db.commit()
                return {"detail": f"Examination {exam_id} deactivated successfully"}
            else:
                db.delete(exam)
                db.commit()
                return {"detail": f"Examination {exam_id} deleted successfully"}
        except Exception:
            db.rollback()
            raise
        finally:
            self._close_db_if_local(db)

    def seed_initial_catalog(self) -> int:
        """Seed initial verified examinations if table is currently empty."""
        db = self._get_db()
        try:
            count = db.execute(select(func.count(Examination.id))).scalar_one()
            if count > 0:
                return 0  # Already seeded

            seeded_count = 0
            for item in SEED_EXAMINATIONS:
                exam = Examination(**item)
                db.add(exam)
                seeded_count += 1

            db.commit()
            return seeded_count
        except Exception:
            db.rollback()
            raise
        finally:
            self._close_db_if_local(db)
