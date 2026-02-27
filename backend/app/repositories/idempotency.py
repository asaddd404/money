from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.idempotency_key import IdempotencyKey

class IdempotencyRepository:
    def __init__(self, db: AsyncSession): self.db=db
    async def get(self, key:str, user_id:int, endpoint:str, method:str):
        q=select(IdempotencyKey).where(IdempotencyKey.key==key, IdempotencyKey.user_id==user_id, IdempotencyKey.endpoint==endpoint, IdempotencyKey.method==method)
        return await self.db.scalar(q)
    async def save(self, **kw): o=IdempotencyKey(**kw); self.db.add(o); await self.db.flush(); return o
