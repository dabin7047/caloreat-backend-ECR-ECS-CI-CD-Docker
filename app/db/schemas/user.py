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
