from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import current_user, db_dep
from app.repositories.wallets import WalletRepository
from app.repositories.transactions import TransactionRepository

router=APIRouter(tags=['wallets'])

@router.get('/students/{student_id}/wallet')
async def wallet(student_id:int, limit:int=20, offset:int=0, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    if user.center_id<=0: raise HTTPException(403,'forbidden')
    w=await WalletRepository(db).get(student_id)
    if not w or w.center_id!=user.center_id: raise HTTPException(404,'wallet not found')
    return {'student_id':w.student_id,'available_balance':w.available_balance,'held_balance':w.held_balance,'total_earned':w.total_earned,'total_spent':w.total_spent}

@router.get('/students/{student_id}/transactions')
async def student_transactions(student_id:int, limit:int=20, offset:int=0, user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    rows=await TransactionRepository(db).list_student(user.center_id, student_id, limit, offset)
    return [{'id':r.id,'type':r.type.value,'amount':r.amount,'reason':r.reason} for r in rows]
