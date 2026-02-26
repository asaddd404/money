from pydantic import BaseModel


class ReviewCreate(BaseModel):
    order_id: int
    rating: int
    comment: str


class ReviewOut(BaseModel):
    id: int
    product_id: int
    order_id: int
    student_id: int
    rating: int
    comment: str
