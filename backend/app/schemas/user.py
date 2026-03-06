from pydantic import BaseModel


class UserMeOut(BaseModel):
    id: int
    center_id: int
    email: str
    full_name: str
    role: str
