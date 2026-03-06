from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product

class ProductRepository:
    def __init__(self, db: AsyncSession): self.db=db
    async def get(self,pid:int): return await self.db.get(Product,pid)
    async def get_for_update(self,pid:int): return await self.db.scalar(select(Product).where(Product.id==pid).with_for_update())
    async def list(self, center_id:int, limit:int, offset:int):
        return (await self.db.scalars(select(Product).where(Product.center_id==center_id).limit(limit).offset(offset))).all()
    async def create(self,**kw): o=Product(**kw); self.db.add(o); await self.db.flush(); return o
