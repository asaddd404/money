from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import current_user, db_dep, idem_header
from app.repositories.enrollments import EnrollmentRepository
from app.services.enrollment_service import EnrollmentService

router=APIRouter(tags=['enrollments'])

@router.post('/groups/{group_id}/enroll')
async def enroll(group_id:int, student_id:int, idempotency_key:str=Depends(idem_header), user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    if user.role.value!='student': raise HTTPException(403,'forbidden')
    svc=EnrollmentService(EnrollmentRepository(db))
    en=await svc.request(user.center_id, student_id, group_id)
    await db.commit(); return {'student_id':en.student_id,'group_id':en.group_id,'center_id':en.center_id,'status':en.status.value}

@router.get('/groups/{group_id}/enrollments')
async def list_group_enrollments(group_id:int, status:str|None=None, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    if user.role.value not in {'teacher','manager','admin'}: raise HTTPException(403,'forbidden')
    rows=await EnrollmentRepository(db).list_by_group(user.center_id, group_id, status)
    return [{'student_id':e.student_id,'group_id':e.group_id,'center_id':e.center_id,'status':e.status.value} for e in rows]

@router.post('/enrollments/{student_id}/{group_id}/approve')
async def approve(student_id:int, group_id:int, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    if user.role.value not in {'teacher','manager','admin'}: raise HTTPException(403,'forbidden')
    en=await EnrollmentService(EnrollmentRepository(db)).approve(user.center_id,student_id,group_id)
    await db.commit(); return {'student_id':en.student_id,'group_id':en.group_id,'center_id':en.center_id,'status':en.status.value}

@router.post('/enrollments/{student_id}/{group_id}/reject')
async def reject(student_id:int, group_id:int, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    if user.role.value not in {'teacher','manager','admin'}: raise HTTPException(403,'forbidden')
    en=await EnrollmentService(EnrollmentRepository(db)).reject(user.center_id,student_id,group_id)
    await db.commit(); return {'student_id':en.student_id,'group_id':en.group_id,'center_id':en.center_id,'status':en.status.value}
