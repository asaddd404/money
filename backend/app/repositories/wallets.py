from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.wallet import Wallet


class WalletRepository:
    def __init__(self, db: AsyncSession): self.db=db
    async def get(self, student_id:int): return await self.db.get(Wallet, student_id)
    async def get_for_update(self, student_id:int):
        return await self.db.scalar(select(Wallet).where(Wallet.student_id==student_id).with_for_update())
    async def create(self, **kw):
        o=Wallet(**kw); self.db.add(o); await self.db.flush(); return o
