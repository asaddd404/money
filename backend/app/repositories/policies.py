from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.teacher_policy import TeacherPolicy

class PolicyRepository:
    def __init__(self, db: AsyncSession): self.db=db
    async def get(self, teacher_id:int): return await self.db.get(TeacherPolicy, teacher_id)
    async def list(self, center_id:int): return (await self.db.scalars(select(TeacherPolicy).where(TeacherPolicy.center_id==center_id))).all()
    async def upsert(self, teacher_id:int, center_id:int, max_points_per_award:int):
        obj=await self.get(teacher_id)
        if not obj:
            obj=TeacherPolicy(teacher_id=teacher_id, center_id=center_id, max_points_per_award=max_points_per_award); self.db.add(obj)
        else: obj.max_points_per_award=max_points_per_award
        await self.db.flush(); return obj
