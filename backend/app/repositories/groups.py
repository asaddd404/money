from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.group import Group


class GroupRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def list(self, center_id: int, limit: int, offset: int):
        q = select(Group).where(Group.center_id == center_id).limit(limit).offset(offset)
        return (await self.db.scalars(q)).all()
    async def get(self, gid: int): return await self.db.get(Group, gid)
    async def create(self, **kw):
        o=Group(**kw); self.db.add(o); await self.db.flush(); return o
