from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def err(code: str, message: str, details: dict | None = None):
    return {'error': {'code': code, 'message': message, 'details': details or {}}}


async def http_exception_handler(_: Request, exc: StarletteHTTPException):
    code_map = {401: 'UNAUTHORIZED', 403: 'FORBIDDEN', 404: 'NOT_FOUND', 409: 'CONFLICT', 422: 'UNPROCESSABLE_ENTITY'}
    return JSONResponse(status_code=exc.status_code, content=err(code_map.get(exc.status_code, 'HTTP_ERROR'), str(exc.detail)))


async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content=err('VALIDATION_ERROR', 'Validation failed', {'issues': exc.errors()}))
