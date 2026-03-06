from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import current_user, db_dep
from app.repositories.policies import PolicyRepository
from app.schemas.policy import TeacherPolicyPatch

router=APIRouter(prefix='/admin/teacher-policies', tags=['admin'])

@router.get('')
async def list_policies(user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    if user.role.value not in {'manager','admin'}: raise HTTPException(403,'forbidden')
    rows=await PolicyRepository(db).list(user.center_id)
    return [{'teacher_id':r.teacher_id,'center_id':r.center_id,'max_points_per_award':r.max_points_per_award} for r in rows]

@router.patch('/{teacher_id}')
async def patch_policy(teacher_id:int,payload:TeacherPolicyPatch,user=Depends(current_user),db:AsyncSession=Depends(db_dep)):
    if user.role.value not in {'manager','admin'}: raise HTTPException(403,'forbidden')
    p=await PolicyRepository(db).upsert(teacher_id,user.center_id,payload.max_points_per_award)
    await db.commit(); return {'teacher_id':p.teacher_id,'center_id':p.center_id,'max_points_per_award':p.max_points_per_award}
