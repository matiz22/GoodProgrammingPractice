from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.sql import func
from db_setup import Base
import os
import hashlib
import binascii

# Password hashing helpers (PBKDF2-HMAC-SHA256)
def hash_password(password: str) -> str:
    """Return salt$hash where both parts are hex-encoded."""
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 260000)
    return binascii.hexlify(salt).decode("ascii") + "$" + binascii.hexlify(dk).decode("ascii")

def verify_password(password: str, stored: str) -> bool:
    """Verify password against stored salt$hash."""
    try:
        salt_hex, hash_hex = stored.split("$", 1)
    except ValueError:
        return False
    salt = binascii.unhexlify(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 260000)
    return binascii.hexlify(dk).decode("ascii") == hash_hex

# New: authentication user table
class AuthUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(512), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
