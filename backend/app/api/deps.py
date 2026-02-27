from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_token
from app.repositories.users import UserRepository

bearer = HTTPBearer(auto_error=False)


async def db_dep(db: AsyncSession = Depends(get_db)):
    return db


async def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: AsyncSession = Depends(get_db)):
    if not credentials:
        raise HTTPException(401, 'missing token')
    payload = decode_token(credentials.credentials)
    if payload.get('type') != 'access':
        raise HTTPException(401, 'invalid token type')
    user = await UserRepository(db).by_id(int(payload['sub']))
    if not user:
        raise HTTPException(401, 'user not found')
    return user


def idem_header(idempotency_key: str | None = Header(default=None, alias='Idempotency-Key')):
    if not idempotency_key:
        raise HTTPException(422, 'Idempotency-Key header required')
    return idempotency_key
