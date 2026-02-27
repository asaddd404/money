from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: int
    stock: int


class ProductPatch(BaseModel):
    name: str | None = None
    price: int | None = None
    stock: int | None = None
    is_active: bool | None = None


class ProductOut(BaseModel):
    id: int
    name: str
    price: int
    stock: int
    is_active: bool
