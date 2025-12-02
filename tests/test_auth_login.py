import os

# ensure SECRET_KEY is available before importing the app / routes
os.environ.setdefault("SECRET_KEY", "testsecret")

from fastapi.testclient import TestClient
# use contextmanager helper for tests
from db_setup import get_session_ctx
from auth.models.user import AuthUser, hash_password
import jwt
import pytest

# import app after SECRET_KEY set
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def ensure_test_user():
    # create or replace a test user in the DB
    with get_session_ctx() as db:
        # remove any existing testuser
        db.query(AuthUser).filter(AuthUser.username == "testuser").delete()
        db.commit()
        user = AuthUser(username="testuser", password_hash=hash_password("secret"), is_admin=False)
        db.add(user)
        db.commit()
        yield
        # cleanup
        db.query(AuthUser).filter(AuthUser.username == "testuser").delete()
        db.commit()

def test_login_success():
    resp = client.post("/login", json={"username": "testuser", "password": "secret"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer"
    # decode token and verify subject
    token = data["access_token"]
    payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=["HS256"])
    assert payload.get("sub") == "testuser"

def test_login_invalid_password():
    resp = client.post("/login", json={"username": "testuser", "password": "wrong"})
    assert resp.status_code == 401

def test_login_missing_fields():
    resp = client.post("/login", json={"username": "testuser"})
    assert resp.status_code == 422
