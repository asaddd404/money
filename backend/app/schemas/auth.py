from pydantic import BaseModel, EmailStr


class RegisterStudentIn(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    center_id: int


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class RefreshIn(BaseModel):
    refresh_token: str


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
