from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.center import Center


class CenterRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def by_id(self, center_id: int):
        return await self.db.get(Center, center_id)

    async def by_name(self, name: str):
        return await self.db.scalar(select(Center).where(Center.name == name))

    async def create(self, name: str, timezone: str = 'UTC'):
        obj = Center(name=name, timezone=timezone)
        self.db.add(obj)
        await self.db.flush()
        return obj
