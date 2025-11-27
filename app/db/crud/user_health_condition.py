from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.user_health_condition import HealthCondition
from app.db.schemas.user_health_condition import (
    HealthConditionCreate,
    HealthConditionUpdate,
    HealthConditionRead,
)
from typing import Optional, List


# 건강 및 식이 제한정보 user_health_conditions
# CRUD db조작 쿼리만 , transaction(x) -> service로 책임 분리
class HealthConditionCrud:

    @staticmethod
    async def create_one_condition_db(db: AsyncSession, condition: dict):
        # model_dump (pytdantic-> dict) : service로이동(user_id필드 추가)
        db_profile = HealthCondition(**condition)
        db.add(db_profile)
        await db.flush()  # PK생성, DB내 query insert
        return db_profile

    # @staticmethod
    # async def create_condition_list_db(
    #     db: AsyncSession, conditions: list[dict]
    # ) -> List[HealthCondition]:
    #     """
    #     conditions=[{"user_id": user_id, "conditions": con} for con in condition_list]
    #     row1 = condition : user_id:6 , condition: diabetes
    #     row2 = condition : user_id:6 , condition: high_blood_pressure
    #     ....
    #     """
    #     db_conditions = [HealthCondition(**condition) for condition in conditions]
    #     db.add_all(db_conditions)
    #     await db.flush()  # PK생성, DB내 query insert

    #     return db_conditions

    # read
    @staticmethod
    async def get_condition_db(db: AsyncSession, user_id: int):
        result = await db.execute(
            select(HealthCondition).where(HealthCondition.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_condition_db(db: AsyncSession, user_id: int) -> bool:
        db_condition = await db.get(HealthCondition, user_id)
        # 실패시 조기종료
        if not db_condition:
            raise HTTPException(status_code=404, detail="Not found")

        await db.delete(db_condition)
        await db.flush()  # db에 쿼리문날림/ 롤백가능
        return True
