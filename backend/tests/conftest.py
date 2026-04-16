"""Pytest configuration: test env must be set before importing the FastAPI app."""

import os
import tempfile

import pytest
from fastapi.testclient import TestClient

# Ephemeral SQLite DB and stable JWT secret for deterministic tests
_fd, _TEST_DB_PATH = tempfile.mkstemp(suffix=".db")
os.close(_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{_TEST_DB_PATH}"
os.environ["JWT_SECRET_KEY"] = "test-jwt-secret-key-at-least-32-bytes-long!!"
os.environ.setdefault("OPENAI_API_KEY", "")

from app.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _init_and_cleanup_test_db():
    """Create tables (TestClient may not run FastAPI startup before DB use)."""
    from app.database import init_db

    init_db()
    yield
    try:
        os.unlink(_TEST_DB_PATH)
    except OSError:
        pass


@pytest.fixture()
def client():
    yield TestClient(app)


@pytest.fixture()
def auth_headers(client):
    """Register a fresh user and return Authorization headers."""
    import uuid

    suffix = uuid.uuid4().hex[:12]
    email = f"user_{suffix}@example.com"
    username = f"u{suffix}"
    password = "Testpw11a"

    reg = client.post(
        "/api/auth/register",
        json={"email": email, "username": username, "password": password},
    )
    assert reg.status_code == 201, reg.text

    login = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
