from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.enrollment import Enrollment


class EnrollmentRepository:
    def __init__(self, db: AsyncSession): self.db=db
    async def get(self, student_id:int, group_id:int):
        return await self.db.get(Enrollment, {'student_id':student_id,'group_id':group_id})
    async def create(self, **kw):
        o=Enrollment(**kw); self.db.add(o); await self.db.flush(); return o
    async def list_by_group(self, center_id:int, group_id:int, status:str|None):
        q=select(Enrollment).where(Enrollment.center_id==center_id, Enrollment.group_id==group_id)
        if status: q=q.where(Enrollment.status==status)
        return (await self.db.scalars(q)).all()
