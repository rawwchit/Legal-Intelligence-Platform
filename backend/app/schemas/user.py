from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
    
class UserRole(str, Enum):
    ADMIN = "admin"
    LAWYER = "lawyer"
    CLIENT = "client"
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str=Field(min_length=8)
    role: UserRole = UserRole.CLIENT
    
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    model_config = ConfigDict(from_attributes=True)
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
