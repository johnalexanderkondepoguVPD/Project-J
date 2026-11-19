import pytest
from app.Models.examination import Examination
from tests.conftest import TestingSessionLocal


@pytest.fixture
def auth_client(client):
    """Client authenticated with a test user session."""
    client.post("/api/v1/auth/register", json={
        "email": "examiner@example.com",
        "username": "examiner",
        "password": "Password123!",
    })
    return client


def test_seed_initial_catalog(client):
    """Test seeding initial exam catalog is idempotent."""
    res = client.post("/api/v1/exams/seed/initial")
    assert res.status_code == 200
    data = res.json()
    assert data["seeded"] > 0

    # Second call should seed 0 (already seeded)
    res2 = client.post("/api/v1/exams/seed/initial")
    assert res2.status_code == 200
    assert res2.json()["seeded"] == 0


def test_list_examinations_paginated(client):
    """Test list examinations returns proper pagination metadata."""
    client.post("/api/v1/exams/seed/initial")

    response = client.get("/api/v1/exams?page=1&page_size=3")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 3
    assert data["page"] == 1
    assert data["page_size"] == 3
    assert data["total"] >= 6
    assert data["total_pages"] >= 2


def test_search_examinations(client):
    """Test searching by keyword in name or abbreviation."""
    client.post("/api/v1/exams/seed/initial")

    response = client.get("/api/v1/exams?q=UPSC")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    for item in data["items"]:
        assert "UPSC" in item["abbreviation"] or "UPSC" in item["name"] or "UPSC" in item["conducting_body"]


def test_filter_by_exam_type(client):
    """Test filtering examinations by category/type."""
    client.post("/api/v1/exams/seed/initial")

    response = client.get("/api/v1/exams?exam_type=Banking")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    for item in data["items"]:
        assert item["exam_type"] == "Banking"


def test_get_examination_by_id(client):
    """Test retrieving details of an examination by ID."""
    client.post("/api/v1/exams/seed/initial")
    list_res = client.get("/api/v1/exams?page_size=1")
    first_id = list_res.json()["items"][0]["id"]

    response = client.get(f"/api/v1/exams/{first_id}")
    assert response.status_code == 200
    detail = response.json()
    assert detail["id"] == first_id
    assert "syllabus" in detail
    assert "eligibility_criteria" in detail
    assert "exam_pattern" in detail


def test_get_examination_not_found(client):
    """Test 404 response for non-existent examination ID."""
    response = client.get("/api/v1/exams/999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_list_conducting_bodies(client):
    """Test aggregate listing of conducting bodies."""
    client.post("/api/v1/exams/seed/initial")

    response = client.get("/api/v1/exams/bodies")
    assert response.status_code == 200
    bodies = response.json()
    assert len(bodies) > 0
    assert any(b["conducting_body"] == "Union Public Service Commission" for b in bodies)
    assert any(b["conducting_body"] == "Staff Selection Commission" for b in bodies)


def test_create_examination_authenticated(auth_client):
    """Test creating an examination as an authenticated user."""
    payload = {
        "name": "State Administrative Services Exam",
        "abbreviation": "APPSC Group 1",
        "conducting_body": "Andhra Pradesh Public Service Commission",
        "exam_type": "State PSC",
        "level": "State",
        "subject": "General Studies",
        "frequency": "Annual",
        "syllabus": "History and Culture of AP, General Studies, Mental Ability.",
        "official_website": "https://psc.ap.gov.in",
    }
    response = auth_client.post("/api/v1/exams", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["abbreviation"] == "APPSC Group 1"
    assert data["conducting_body"] == "Andhra Pradesh Public Service Commission"
    assert data["id"] is not None


def test_create_examination_unauthenticated(client):
    """Test creating an exam without authentication returns 401."""
    payload = {
        "name": "Test Exam",
        "conducting_body": "Test Body",
        "exam_type": "Test",
        "level": "National",
    }
    response = client.post("/api/v1/exams", json=payload)
    assert response.status_code == 401


def test_create_duplicate_abbreviation(auth_client):
    """Test rejection when creating an exam with already existing abbreviation."""
    auth_client.post("/api/v1/exams/seed/initial")

    payload = {
        "name": "Duplicate UPSC",
        "abbreviation": "UPSC CSE",
        "conducting_body": "Another Body",
        "exam_type": "UPSC",
        "level": "National",
    }
    response = auth_client.post("/api/v1/exams", json=payload)
    assert response.status_code == 422
    assert "already exists" in response.json()["detail"]


def test_update_examination(auth_client):
    """Test updating an existing examination."""
    auth_client.post("/api/v1/exams/seed/initial")
    list_res = auth_client.get("/api/v1/exams?q=NEET")
    neet_id = list_res.json()["items"][0]["id"]

    update_payload = {
        "syllabus": "Updated syllabus for Class 11 and 12 physics, chemistry, biology."
    }
    response = auth_client.put(f"/api/v1/exams/{neet_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["syllabus"] == update_payload["syllabus"]


def test_delete_examination_soft(auth_client):
    """Test soft-deleting an examination sets is_active=False."""
    auth_client.post("/api/v1/exams/seed/initial")
    list_res = auth_client.get("/api/v1/exams?q=NTPC")
    ntpc_id = list_res.json()["items"][0]["id"]

    del_res = auth_client.delete(f"/api/v1/exams/{ntpc_id}?soft=true")
    assert del_res.status_code == 200

    # Querying active exams should no longer include it
    active_res = auth_client.get("/api/v1/exams?is_active=true")
    assert not any(item["id"] == ntpc_id for item in active_res.json()["items"])
