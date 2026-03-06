from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import current_user, db_dep
from app.repositories.audits import AuditRepository

router=APIRouter(prefix='/admin', tags=['admin'])

@router.get('/audit-logs')
async def audit_logs(limit:int=20, offset:int=0, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    if user.role.value not in {'manager','admin'}: raise HTTPException(403,'forbidden')
    rows=await AuditRepository(db).list(user.center_id,limit,offset)
    return [{'id':a.id,'action':a.action,'entity_type':a.entity_type,'entity_id':a.entity_id,'payload':a.payload} for a in rows]
