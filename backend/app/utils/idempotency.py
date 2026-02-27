from fastapi import HTTPException


def require_idempotency_key(value: str | None):
    if not value:
        raise HTTPException(status_code=422, detail='Idempotency-Key header required')
