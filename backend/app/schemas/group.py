from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str
    owner_teacher_id: int


class GroupPatch(BaseModel):
    name: str | None = None
    owner_teacher_id: int | None = None


class GroupOut(BaseModel):
    id: int
    center_id: int
    name: str
    owner_teacher_id: int
