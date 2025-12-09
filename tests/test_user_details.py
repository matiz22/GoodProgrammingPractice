import os

# ensure SECRET_KEY is available before importing the app / routes
os.environ.setdefault("SECRET_KEY", "testsecret")

from fastapi.testclient import TestClient
from db_setup import get_session_ctx
from auth.models.user import AuthUser, hash_password
import pytest
import jwt

# import app after SECRET_KEY set
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def ensure_detail_user():
    with get_session_ctx() as db:
        db.query(AuthUser).filter(AuthUser.username == "detailuser").delete()
        db.commit()
        user = AuthUser(username="detailuser", password_hash=hash_password("detailpass"), is_admin=True)
        db.add(user)
        db.commit()
        yield
        db.query(AuthUser).filter(AuthUser.username == "detailuser").delete()
        db.commit()

def login_and_get_token(username="detailuser", password="detailpass"):
    resp = client.post("/login", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]

def test_user_details_success():
    token = login_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/user_details", headers=headers)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["username"] == "detailuser"
    assert "id" in data
    assert data["is_admin"] is True

def test_user_details_invalid_token():
    headers = {"Authorization": "Bearer invalid.token.here"}
    resp = client.get("/user_details", headers=headers)
    assert resp.status_code == 401

def test_user_details_missing_token():
    resp = client.get("/user_details")
    # HTTPBearer returns 403 when credentials are missing
    assert resp.status_code == 403

