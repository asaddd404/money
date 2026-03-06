from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import current_user, db_dep, idem_header
from app.repositories.groups import GroupRepository
from app.repositories.enrollments import EnrollmentRepository
from app.repositories.wallets import WalletRepository
from app.repositories.transactions import TransactionRepository
from app.repositories.policies import PolicyRepository
from app.repositories.idempotency import IdempotencyRepository
from app.repositories.audits import AuditRepository
from app.schemas.transaction import AwardIn
from app.services.award_service import AwardService
from app.services.audit_service import AuditService

router=APIRouter(tags=['awards'])

@router.post('/awards')
async def award(payload:AwardIn, idempotency_key:str=Depends(idem_header), user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    svc=AwardService(GroupRepository(db),EnrollmentRepository(db),WalletRepository(db),TransactionRepository(db),PolicyRepository(db),IdempotencyRepository(db),AuditService(AuditRepository(db)))
    code,body=await svc.award(user,idempotency_key,'/api/v1/awards','POST',payload.student_id,payload.group_id,payload.amount,payload.reason)
    await db.commit(); return JSONResponse(status_code=code,content=body)
