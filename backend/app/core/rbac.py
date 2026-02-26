from fastapi import HTTPException, status


def require_roles(user_role: str, allowed: set[str]) -> None:
    if user_role not in allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='forbidden')
