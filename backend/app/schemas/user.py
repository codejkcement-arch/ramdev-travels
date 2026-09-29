from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str | None = None
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None
    is_admin: bool
    model_config = {"from_attributes": True}
