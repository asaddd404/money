import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from argon2 import PasswordHasher
from app.core.config import get_settings

settings = get_settings()
ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        return ph.verify(hashed, password)
    except Exception:
        return False


def create_token(subject: str, token_type: str, ttl_minutes: int, jti: str | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'sub': subject,
        'type': token_type,
        'iat': int(now.timestamp()),
        'exp': int((now + timedelta(minutes=ttl_minutes)).timestamp()),
        'jti': jti or secrets.token_urlsafe(16),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise ValueError('invalid token') from exc


def refresh_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
