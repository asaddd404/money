from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.refresh_token import RefreshToken

class RefreshTokenRepository:
    def __init__(self, db: AsyncSession): self.db=db
    async def create(self, **kw): o=RefreshToken(**kw); self.db.add(o); await self.db.flush(); return o
    async def by_hash(self, token_hash:str): return await self.db.scalar(select(RefreshToken).where(RefreshToken.token_hash==token_hash))
    async def revoke(self, token: RefreshToken): token.revoked_at=datetime.now(timezone.utc); await self.db.flush()
