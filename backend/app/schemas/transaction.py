from pydantic import BaseModel


class AwardIn(BaseModel):
    student_id: int
    group_id: int
    amount: int
    reason: str


class TransactionOut(BaseModel):
    id: int
    type: str
    amount: int
    reason: str
