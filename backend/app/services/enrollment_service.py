from fastapi import HTTPException
from app.models.enrollment import EnrollmentStatus
from app.repositories.enrollments import EnrollmentRepository


class EnrollmentService:
    def __init__(self, repo: EnrollmentRepository): self.repo=repo

    async def request(self, center_id:int, student_id:int, group_id:int):
        en=await self.repo.get(student_id, group_id)
        if en: return en
        return await self.repo.create(center_id=center_id, student_id=student_id, group_id=group_id, status=EnrollmentStatus.pending)

    async def approve(self, center_id:int, student_id:int, group_id:int):
        en=await self.repo.get(student_id,group_id)
        if not en or en.center_id!=center_id: raise HTTPException(404,'enrollment not found')
        en.status=EnrollmentStatus.approved
        return en

    async def reject(self, center_id:int, student_id:int, group_id:int):
        en=await self.repo.get(student_id,group_id)
        if not en or en.center_id!=center_id: raise HTTPException(404,'enrollment not found')
        en.status=EnrollmentStatus.rejected
        return en
