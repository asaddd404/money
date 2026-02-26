from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.review import Review

class ReviewRepository:
    def __init__(self, db: AsyncSession): self.db=db
    async def create(self, **kw): o=Review(**kw); self.db.add(o); await self.db.flush(); return o
    async def list_by_product(self, center_id:int, product_id:int):
        return (await self.db.scalars(select(Review).where(Review.center_id==center_id, Review.product_id==product_id))).all()
