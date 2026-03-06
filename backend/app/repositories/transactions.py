from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import Transaction, TransactionType

class TransactionRepository:
    def __init__(self, db: AsyncSession): self.db=db
    async def create(self, **kw): o=Transaction(**kw); self.db.add(o); await self.db.flush(); return o
    async def list_student(self, center_id:int, student_id:int, limit:int, offset:int):
        q=select(Transaction).where(Transaction.center_id==center_id, Transaction.student_id==student_id).limit(limit).offset(offset)
        return (await self.db.scalars(q)).all()
    async def leaderboard(self, center_id:int, start, end, group_id:int|None=None):
        q=select(Transaction.student_id, func.sum(Transaction.amount).label('score'), func.max(Transaction.awarded_at).label('last_award')).where(
            Transaction.center_id==center_id, Transaction.type==TransactionType.award, Transaction.awarded_at>=start, Transaction.awarded_at<end
        )
        if group_id: q=q.where(Transaction.group_id==group_id)
        q=q.group_by(Transaction.student_id).order_by(func.sum(Transaction.amount).desc(), func.max(Transaction.awarded_at).desc())
        return (await self.db.execute(q)).all()
