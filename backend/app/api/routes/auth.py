from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import db_dep
from app.core.config import get_settings
from app.repositories.users import UserRepository
from app.repositories.wallets import WalletRepository
from app.repositories.refresh_tokens import RefreshTokenRepository
from app.schemas.auth import RegisterStudentIn, LoginIn, RefreshIn, TokenOut
from app.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/register-student')
async def register_student(payload: RegisterStudentIn, db: AsyncSession = Depends(db_dep)):
    svc=AuthService(UserRepository(db), WalletRepository(db), RefreshTokenRepository(db))
    u=await svc.register_student(payload.email,payload.password,payload.full_name,payload.center_id)
    await db.commit(); return {'id':u.id,'email':u.email}

@router.post('/login', response_model=TokenOut)
async def login(payload: LoginIn, db: AsyncSession = Depends(db_dep)):
    s=get_settings(); svc=AuthService(UserRepository(db), WalletRepository(db), RefreshTokenRepository(db))
    a,r=await svc.login(payload.email,payload.password,s.access_token_minutes,s.refresh_token_days)
    await db.commit(); return {'access_token':a,'refresh_token':r}

@router.post('/refresh', response_model=TokenOut)
async def refresh(payload: RefreshIn, db: AsyncSession = Depends(db_dep)):
    s=get_settings(); svc=AuthService(UserRepository(db), WalletRepository(db), RefreshTokenRepository(db))
    a,r=await svc.refresh(payload.refresh_token,s.access_token_minutes,s.refresh_token_days)
    await db.commit(); return {'access_token':a,'refresh_token':r}

@router.post('/logout')
async def logout(payload: RefreshIn, db: AsyncSession = Depends(db_dep)):
    svc=AuthService(UserRepository(db), WalletRepository(db), RefreshTokenRepository(db))
    await svc.logout(payload.refresh_token); await db.commit(); return {'ok':True}
