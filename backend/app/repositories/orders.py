from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import Order, OrderItem

class OrderRepository:
    def __init__(self, db: AsyncSession): self.db=db
    async def get(self, oid:int): return await self.db.get(Order, oid)
    async def list(self, center_id:int, limit:int, offset:int):
        return (await self.db.scalars(select(Order).where(Order.center_id==center_id).limit(limit).offset(offset))).all()
    async def create(self, **kw): o=Order(**kw); self.db.add(o); await self.db.flush(); return o
    async def add_item(self, **kw): self.db.add(OrderItem(**kw)); await self.db.flush()
