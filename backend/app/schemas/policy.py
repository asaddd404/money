from pydantic import BaseModel


class TeacherPolicyPatch(BaseModel):
    max_points_per_award: int


class TeacherPolicyOut(BaseModel):
    teacher_id: int
    center_id: int
    max_points_per_award: int
