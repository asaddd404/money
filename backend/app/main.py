from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.config import get_settings
from app.core.errors import http_exception_handler, validation_exception_handler
from app.core.logging import setup_logging
from app.core.middleware import RequestContextMiddleware
from app.api.routes import auth, users, groups, enrollments, awards, wallets, products, orders, reviews, leaderboards, admin_policies, admin_audit

settings = get_settings()
setup_logging()
app = FastAPI(title=settings.app_name)
app.add_middleware(RequestContextMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=[i.strip() for i in settings.cors_origins.split(',') if i.strip()], allow_methods=['*'], allow_headers=['*'])
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(users.router, prefix=settings.api_prefix)
app.include_router(groups.router, prefix=settings.api_prefix)
app.include_router(enrollments.router, prefix=settings.api_prefix)
app.include_router(awards.router, prefix=settings.api_prefix)
app.include_router(wallets.router, prefix=settings.api_prefix)
app.include_router(products.router, prefix=settings.api_prefix)
app.include_router(orders.router, prefix=settings.api_prefix)
app.include_router(reviews.router, prefix=settings.api_prefix)
app.include_router(leaderboards.router, prefix=settings.api_prefix)
app.include_router(admin_policies.router, prefix=settings.api_prefix)
app.include_router(admin_audit.router, prefix=settings.api_prefix)

@app.get('/health')
async def health():
    return {'ok': True}
