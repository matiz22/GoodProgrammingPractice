import os

# ensure SECRET_KEY is available before importing the app / routes
os.environ.setdefault("SECRET_KEY", "testsecret")

from fastapi.testclient import TestClient
from db_setup import get_session_ctx
from auth.models.user import AuthUser, hash_password
import pytest

# import app after SECRET_KEY set
from main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_users():
    # create admin and non-admin users
    with get_session_ctx() as db:
        # cleanup any leftovers
        db.query(AuthUser).filter(AuthUser.username.in_(["adminuser", "regularuser", "newuser"])).delete(synchronize_session=False)
        db.commit()
        admin = AuthUser(username="adminuser", password_hash=hash_password("adminpass"), is_admin=True)
        regular = AuthUser(username="regularuser", password_hash=hash_password("regularpass"), is_admin=False)
        db.add_all([admin, regular])
        db.commit()
    yield
    # teardown
    with get_session_ctx() as db:
        db.query(AuthUser).filter(AuthUser.username.in_(["adminuser", "regularuser", "newuser"])).delete(synchronize_session=False)
        db.commit()

def login_and_get_token(username, password):
    resp = client.post("/login", json={"username": username, "password": password})
    assert resp.status_code == 200, f"login failed for {username}: {resp.text}"
    return resp.json()["access_token"]

def test_admin_can_create_user(setup_users):
    admin_token = login_and_get_token("adminuser", "adminpass")
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {"username": "newuser", "password": "newpass"}
    resp = client.post("/users/", json=payload, headers=headers)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["username"] == "newuser"
    assert data["is_admin"] is False

    # duplicate attempt by admin -> 400
    resp2 = client.post("/users/", json=payload, headers=headers)
    assert resp2.status_code == 400

def test_regular_cannot_create_user(setup_users):
    regular_token = login_and_get_token("regularuser", "regularpass")
    headers = {"Authorization": f"Bearer {regular_token}"}
    payload = {"username": "anotheruser", "password": "anotherpass"}
    resp = client.post("/users/", json=payload, headers=headers)
    assert resp.status_code == 403

