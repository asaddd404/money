from pydantic import BaseModel


class EnrollmentRequestIn(BaseModel):
    student_id: int


class EnrollmentOut(BaseModel):
    student_id: int
    group_id: int
    center_id: int
    status: str
