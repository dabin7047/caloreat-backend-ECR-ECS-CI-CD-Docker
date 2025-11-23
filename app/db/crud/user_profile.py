from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.user import User
from app.db.schemas.user import UserCreate, UserUpdate
from typing import Optional, List

# UserProfile or UserInfo


class UserProfileCrud:
    # create
    @staticmethod
    async def create_profile():
        pass

    # read me
    @staticmethod
    async def get_profile():
        pass

    # update
    @staticmethod
    async def update_profile():
        pass

    # delete 필요 x : 유저삭제시에만 프로필 삭제됨
