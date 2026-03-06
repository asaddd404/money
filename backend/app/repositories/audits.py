from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog

class AuditRepository:
    def __init__(self, db: AsyncSession): self.db=db
    async def create(self, **kw): o=AuditLog(**kw); self.db.add(o); await self.db.flush(); return o
    async def list(self, center_id:int, limit:int, offset:int):
        return (await self.db.scalars(select(AuditLog).where(AuditLog.center_id==center_id).limit(limit).offset(offset))).all()
