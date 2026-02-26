from fastapi import HTTPException
from app.models.enrollment import EnrollmentStatus
from app.models.transaction import TransactionType
from app.repositories.groups import GroupRepository
from app.repositories.enrollments import EnrollmentRepository
from app.repositories.wallets import WalletRepository
from app.repositories.transactions import TransactionRepository
from app.repositories.policies import PolicyRepository
from app.repositories.idempotency import IdempotencyRepository
from app.services.audit_service import AuditService
from app.utils.time import now_utc


class AwardService:
    def __init__(self, groups, enrollments, wallets, tx, policies, idem, audits):
        self.groups: GroupRepository=groups; self.enrollments: EnrollmentRepository=enrollments; self.wallets: WalletRepository=wallets
        self.tx: TransactionRepository=tx; self.policies: PolicyRepository=policies; self.idem: IdempotencyRepository=idem; self.audits: AuditService=audits

    async def award(self, actor, idem_key:str, endpoint:str, method:str, student_id:int, group_id:int, amount:int, reason:str):
        cached = await self.idem.get(idem_key, actor.id, endpoint, method)
        if cached: return cached.status_code, cached.response_body
        if actor.role not in {'teacher','manager','admin'}: raise HTTPException(403,'forbidden')
        g=await self.groups.get(group_id)
        if not g or g.center_id!=actor.center_id: raise HTTPException(404,'group not found')
        if actor.role=='teacher' and g.owner_teacher_id!=actor.id: raise HTTPException(403,'teacher can award own group only')
        en=await self.enrollments.get(student_id,group_id)
        if not en or en.status!=EnrollmentStatus.approved: raise HTTPException(403,'enrollment not approved')
        if amount<=0: raise HTTPException(422,'amount must be positive')
        p=await self.policies.get(actor.id)
        if actor.role=='teacher' and p and amount>p.max_points_per_award: raise HTTPException(422,'amount exceeds teacher policy')
        wallet=await self.wallets.get_for_update(student_id)
        wallet.available_balance += amount; wallet.total_earned += amount
        tr=await self.tx.create(center_id=actor.center_id, student_id=student_id, group_id=group_id, type=TransactionType.award, amount=amount, reason=reason,
            awarded_by=actor.id, award_date=now_utc().date(), awarded_at=now_utc(), available_after=wallet.available_balance, held_after=wallet.held_balance)
        await self.audits.log(actor.center_id, actor.id, 'award_coins', 'transaction', str(tr.id), {'amount': amount, 'reason': reason})
        body={'id':tr.id,'type':'award','amount':amount,'reason':reason}
        await self.idem.save(key=idem_key, user_id=actor.id, endpoint=endpoint, method=method, status_code=200, response_body=body)
        return 200, body
