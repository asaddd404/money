from pydantic import BaseModel


class OrderItemIn(BaseModel):
    product_id: int
    quantity: int


class OrderCreateIn(BaseModel):
    items: list[OrderItemIn]


class OrderOut(BaseModel):
    id: int
    student_id: int
    status: str
    total_amount: int
