from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

class AuthUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUser

class RegisterInput(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class BookPublic(BaseModel):
    id: int
    title: str
    author: str
    category: str
    description: str
    owner_id: int
    status: str
    created_at: datetime
