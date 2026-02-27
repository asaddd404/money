from datetime import timedelta
from fastapi import HTTPException
from app.core.security import hash_password, verify_password, create_token, decode_token, refresh_hash
from app.repositories.users import UserRepository
from app.repositories.wallets import WalletRepository
from app.repositories.refresh_tokens import RefreshTokenRepository
from app.models.user import UserRole
from app.utils.time import now_utc


class AuthService:
    def __init__(self, users:UserRepository, wallets:WalletRepository, refresh_repo:RefreshTokenRepository):
        self.users=users; self.wallets=wallets; self.refresh_repo=refresh_repo

    async def register_student(self, email:str, password:str, full_name:str, center_id:int):
        if await self.users.by_email(email): raise HTTPException(409,'email already used')
        user = await self.users.create(email=email, password_hash=hash_password(password), full_name=full_name, center_id=center_id, role=UserRole.student)
        await self.wallets.create(student_id=user.id, center_id=center_id)
        return user

    async def login(self, email:str, password:str, access_minutes:int, refresh_days:int):
        u=await self.users.by_email(email)
        if not u or not verify_password(password,u.password_hash): raise HTTPException(401,'invalid credentials')
        access=create_token(str(u.id), 'access', access_minutes)
        refresh=create_token(str(u.id), 'refresh', refresh_days*24*60)
        payload=decode_token(refresh)
        await self.refresh_repo.create(user_id=u.id, jti=payload['jti'], token_hash=refresh_hash(refresh), expires_at=now_utc()+timedelta(days=refresh_days))
        return access, refresh

    async def refresh(self, refresh_token:str, access_minutes:int, refresh_days:int):
        payload=decode_token(refresh_token)
        if payload.get('type')!='refresh': raise HTTPException(401,'invalid refresh token')
        row=await self.refresh_repo.by_hash(refresh_hash(refresh_token))
        if not row or row.revoked_at is not None: raise HTTPException(401,'refresh token revoked')
        await self.refresh_repo.revoke(row)
        access=create_token(payload['sub'], 'access', access_minutes)
        new_refresh=create_token(payload['sub'], 'refresh', refresh_days*24*60)
        new_payload=decode_token(new_refresh)
        await self.refresh_repo.create(user_id=int(payload['sub']), jti=new_payload['jti'], token_hash=refresh_hash(new_refresh), expires_at=now_utc()+timedelta(days=refresh_days))
        return access, new_refresh

    async def logout(self, refresh_token:str):
        row=await self.refresh_repo.by_hash(refresh_hash(refresh_token))
        if row and row.revoked_at is None: await self.refresh_repo.revoke(row)
