from pydantic import BaseModel, EmailStr, ConfigDict
import uuid
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    timezone: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str | None = None
    exp: int | None = None
