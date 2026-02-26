from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession): self.db = db

    async def by_email(self, email: str):
        return await self.db.scalar(select(User).where(User.email == email))

    async def by_id(self, user_id: int):
        return await self.db.get(User, user_id)

    async def create(self, **kwargs):
        obj = User(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj
