import pytest
from app.core.config import settings
from app.Models.user import User
from app.services.auth import get_password_hash
from tests.conftest import TestingSessionLocal


def test_register_success(client):
    """Test successful user registration sets cookie and returns user."""
    payload = {
        "email": "testuser@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "Password123!",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["username"] == "testuser"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data

    # Verify session cookie was set
    cookie_name = settings.session_cookie_name
    assert cookie_name in response.cookies or "session_id" in response.cookies


def test_register_duplicate_email(client):
    """Test registration rejects duplicate email."""
    payload = {
        "email": "duplicate@example.com",
        "username": "userone",
        "password": "Password123!",
    }
    res1 = client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    payload2 = {
        "email": "duplicate@example.com",
        "username": "usertwo",
        "password": "Password123!",
    }
    res2 = client.post("/api/v1/auth/register", json=payload2)
    assert res2.status_code == 422
    assert "Email already registered" in res2.json()["detail"]


def test_register_duplicate_username(client):
    """Test registration rejects duplicate username."""
    payload = {
        "email": "user1@example.com",
        "username": "sameuser",
        "password": "Password123!",
    }
    res1 = client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    payload2 = {
        "email": "user2@example.com",
        "username": "sameuser",
        "password": "Password123!",
    }
    res2 = client.post("/api/v1/auth/register", json=payload2)
    assert res2.status_code == 422
    assert "Username already taken" in res2.json()["detail"]


def test_register_short_password(client):
    """Test registration rejects password under 8 characters."""
    payload = {
        "email": "short@example.com",
        "username": "shortpass",
        "password": "123",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422


def test_login_with_email_success(client):
    """Test login using email identifier."""
    # Register first
    client.post("/api/v1/auth/register", json={
        "email": "loginuser@example.com",
        "username": "loginuser",
        "password": "ValidPassword123!",
    })

    # Login
    response = client.post("/api/v1/auth/login", json={
        "identifier": "loginuser@example.com",
        "password": "ValidPassword123!",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "loginuser@example.com"
    assert data["username"] == "loginuser"


def test_login_with_username_success(client):
    """Test login using username identifier."""
    client.post("/api/v1/auth/register", json={
        "email": "username_login@example.com",
        "username": "uniquename",
        "password": "ValidPassword123!",
    })

    response = client.post("/api/v1/auth/login", json={
        "identifier": "uniquename",
        "password": "ValidPassword123!",
    })
    assert response.status_code == 200
    assert response.json()["username"] == "uniquename"


def test_login_invalid_password(client):
    """Test login with wrong password returns 401."""
    client.post("/api/v1/auth/register", json={
        "email": "wrongpass@example.com",
        "username": "wrongpass",
        "password": "CorrectPassword123!",
    })

    response = client.post("/api/v1/auth/login", json={
        "identifier": "wrongpass@example.com",
        "password": "WrongPassword999!",
    })
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test login for nonexistent user returns 401."""
    response = client.post("/api/v1/auth/login", json={
        "identifier": "nobody@example.com",
        "password": "SomePassword123!",
    })
    assert response.status_code == 401


def test_login_disabled_account(client):
    """Test disabled account cannot log in."""
    # Register first
    reg = client.post("/api/v1/auth/register", json={
        "email": "disabled@example.com",
        "username": "disableduser",
        "password": "ValidPassword123!",
    })
    assert reg.status_code == 201

    # Disable user in DB
    db = TestingSessionLocal()
    from sqlalchemy import update
    db.execute(update(User).where(User.username == "disableduser").values(is_active=False))
    db.commit()
    db.close()

    response = client.post("/api/v1/auth/login", json={
        "identifier": "disabled@example.com",
        "password": "ValidPassword123!",
    })
    assert response.status_code == 401
    assert "disabled" in response.json()["detail"].lower()


def test_me_authenticated(client):
    """Test /me returns authenticated user when session cookie is provided."""
    # Register sets the session cookie in client
    client.post("/api/v1/auth/register", json={
        "email": "profile@example.com",
        "username": "profileuser",
        "password": "Password123!",
    })

    response = client.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert response.json()["username"] == "profileuser"


def test_me_authenticated_via_bearer_token(client):
    """Test /me returns authenticated user when session token is provided via Authorization header."""
    reg = client.post("/api/v1/auth/register", json={
        "email": "bearer@example.com",
        "username": "beareruser",
        "password": "Password123!",
    })
    assert reg.status_code == 201

    cookie_name = settings.session_cookie_name
    session_id = reg.cookies.get(cookie_name) or reg.cookies.get("session_id")
    assert session_id is not None

    # Clear client cookies to ensure authentication relies solely on Authorization header
    client.cookies.clear()

    # Pass Authorization Bearer
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {session_id}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "beareruser"


def test_me_unauthenticated(client):
    """Test /me returns 401 when unauthenticated."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_logout_revokes_session(client):
    """Test logout revokes the session and clears access."""
    # Register and verify /me works
    client.post("/api/v1/auth/register", json={
        "email": "logout@example.com",
        "username": "logoutuser",
        "password": "Password123!",
    })
    me_before = client.get("/api/v1/auth/me")
    assert me_before.status_code == 200

    # Logout
    logout_res = client.post("/api/v1/auth/logout")
    assert logout_res.status_code == 200

    # Subsequent /me should now fail
    me_after = client.get("/api/v1/auth/me")
    assert me_after.status_code == 401
