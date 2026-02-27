from app.repositories.transactions import TransactionRepository
from app.utils.time import period_bounds


class LeaderboardService:
    def __init__(self, tx: TransactionRepository): self.tx=tx

    async def group(self, center_id:int, timezone:str, group_id:int, period:str):
        start,end=period_bounds(period, timezone)
        return await self.tx.leaderboard(center_id,start,end,group_id)

    async def global_board(self, center_id:int, timezone:str, period:str):
        start,end=period_bounds(period, timezone)
        return await self.tx.leaderboard(center_id,start,end,None)
