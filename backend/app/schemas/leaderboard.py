from pydantic import BaseModel


class LeaderboardRow(BaseModel):
    student_id: int
    score: int
    last_award: str | None = None
