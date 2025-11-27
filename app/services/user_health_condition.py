from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas.user_health_condition import (
    HealthConditionCreate,
    HealthConditionUpdate,
    HealthConditionRead,
)
from app.db.models.user import User
from app.db.models.user_health_condition import HealthCondition
from app.db.crud.user_health_condition import HealthConditionCrud

from enum import Enum
from datetime import date

# 건강 및 식이 제한정보 user_health_conditions


class HealthConditionService:
    @staticmethod
    async def create_condition(
        db: AsyncSession, user_id: int, conditions: HealthConditionCreate
    ):
        pass

    @staticmethod
    async def read_condition(db: AsyncSession, user_id: int):
        pass

    @staticmethod
    async def update_condition(
        db: AsyncSession, user_id: int, conditions: HealthConditionUpdate
    ):
        pass

    @staticmethod
    async def delete_condition(db, user_id):
        pass
