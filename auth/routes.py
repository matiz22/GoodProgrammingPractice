from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
# use get_session (dependency generator) from db_setup
from db_setup import SessionLocal, engine, Base, get_session
# use relative imports so the package modules are found
from .models.user import AuthUser, hash_password, verify_password
from .models.user_request import UserCreate, UserOut
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import os
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv

# load .env so SECRET_KEY can come from there
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = None

# ensure table for AuthUser exists
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/users", tags=["users"])

# add bearer auth scheme
bearer_scheme = HTTPBearer()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    # validate token and ensure requester is admin
    if SECRET_KEY is None:
        raise HTTPException(status_code=500, detail="SECRET_KEY not configured")
    token = credentials.credentials
    try:
        token_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        requester_username = token_payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="invalid token")

    if not requester_username:
        raise HTTPException(status_code=401, detail="invalid token")

    requester = db.query(AuthUser).filter(AuthUser.username == requester_username).first()
    if not requester or not requester.is_admin:
        raise HTTPException(status_code=403, detail="admin privileges required")

    # check existing username
    existing = db.query(AuthUser).filter(AuthUser.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="username already exists")
    # hash password and create user
    pw_hash = hash_password(payload.password)
    user = AuthUser(username=payload.username, password_hash=pw_hash)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="username already exists")
    return UserOut(id=user.id, username=user.username, is_admin=user.is_admin)

# New: separate router for auth endpoints (so we can expose /login at root)
auth_router = APIRouter(tags=["auth"])

# New: proper Pydantic model for login request
class LoginRequest(BaseModel):
    username: str
    password: str

# Add login POST endpoint
@auth_router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_session)):
    """
    Request body: {"username": "user", "password": "pass"}
    Returns: {"access_token": "<jwt>", "token_type": "bearer"}
    """
    if SECRET_KEY is None:
        raise HTTPException(status_code=500, detail="SECRET_KEY not configured")

    username = payload.username
    password = payload.password
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")

    user = db.query(AuthUser).filter(AuthUser.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="invalid credentials")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")

    expire = datetime.utcnow() + timedelta(minutes=30)
    token_payload = {"sub": user.username, "exp": expire}
    token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

# New endpoint: return details about the logged-in user
@auth_router.get("/user_details", response_model=UserOut)
def user_details(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_session),
):
    if SECRET_KEY is None:
        raise HTTPException(status_code=500, detail="SECRET_KEY not configured")
    token = credentials.credentials
    try:
        token_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = token_payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="invalid token")

    if not username:
        raise HTTPException(status_code=401, detail="invalid token")

    user = db.query(AuthUser).filter(AuthUser.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="invalid token")

    return UserOut(id=user.id, username=user.username, is_admin=user.is_admin)
