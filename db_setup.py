from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

SQLALCHEMY_DATABASE_URL = "sqlite:///./movies.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# New: FastAPI dependency (generator) that yields a Session instance for Depends(...)
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# keep a contextmanager for test code that uses: with get_session_ctx() as db:
@contextmanager
def get_session_ctx():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def create_db():
    Base.metadata.create_all(bind=engine)
