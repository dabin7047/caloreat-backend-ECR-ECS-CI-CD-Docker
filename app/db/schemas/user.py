from pydantic import BaseModel, EmailStr
from typing import Optional, List

#UserBase
class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    pass

class UserInDB(BaseModel):
    pass

    class Config:
        from_attributes=True
        # populate_by_name=True  #향후 호환 문제시 사용

class UserRead(UserInDB):
    pass

# login
#login-직원만 전화번호/비밀번호
class StaffLogin(BaseModel):    
    phone:str|None = None
    password:str|None = None   

#AuthResponse
class PrivateUserRead(BaseModel):
    user_id: int
    name: str
    phone: str
    address: str
    is_staff: bool

    class Config:
        from_attributes = True
class AuthResponse(BaseModel):
        verified_staff:PrivateUserRead
        access_token: str
        refresh_token: str