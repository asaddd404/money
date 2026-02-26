from pydantic import BaseModel


class WalletOut(BaseModel):
    student_id: int
    available_balance: int
    held_balance: int
    total_earned: int
    total_spent: int
