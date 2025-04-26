from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    username: str
    password: str
    token_name: str  # Nuevo campo

class Login(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    api_token: str  # Nuevo campo
    token_name: str
    created_at: datetime
    partial_token: str
    
    class Config:
        from_attributes = True

# Mantener los demás schemas igual...
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    username: str | None = None

class TokenResponse(BaseModel):
    api_token: str
    token_name: str
    created_at: datetime
    partial_token: str
    
    class Config:
        from_attributes = True