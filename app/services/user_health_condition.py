from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas.user_profile import (
    UserProfileCreate,
    UserProfileRead,
    UserProfileUpdate,
)
from app.db.models.user_profile import UserProfile
from app.db.crud.user_profile import UserProfileCrud

from enum import Enum
from datetime import date

# 건강 및 식이 제한정보 user_health_conditions


class HealthConditionService:
    @staticmethod
    async def create_condition(db, current_user_id):
        pass

    @staticmethod
    async def read_condition():
        pass

    @staticmethod
    async def update_condition():
        pass

    @staticmethod
    async def delete_condition(db, current_user_id):
        pass
