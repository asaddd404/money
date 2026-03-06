from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import current_user, db_dep
from app.repositories.transactions import TransactionRepository
from app.services.leaderboard_service import LeaderboardService

router=APIRouter(prefix='/leaderboards', tags=['leaderboards'])

@router.get('/group/{group_id}')
async def group_lb(group_id:int, period:str='day', user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    rows=await LeaderboardService(TransactionRepository(db)).group(user.center_id,'UTC',group_id,period)
    return [{'student_id':r[0],'score':int(r[1]),'last_award':str(r[2]) if r[2] else None} for r in rows]

@router.get('/global')
async def global_lb(period:str='day', user=Depends(current_user), db:AsyncSession=Depends(db_dep)):
    rows=await LeaderboardService(TransactionRepository(db)).global_board(user.center_id,'UTC',period)
    return [{'student_id':r[0],'score':int(r[1]),'last_award':str(r[2]) if r[2] else None} for r in rows]
