from pydantic import BaseModel, EmailStr
from enums.roles import UserRole    

class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: UserRole

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: UserRole

class RoleUpdate(BaseModel):
    role: UserRole

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True