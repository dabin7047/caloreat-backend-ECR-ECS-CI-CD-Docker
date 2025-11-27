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
# 최소 기능 구현상태 - error 터지면 아마도 500 -> 일단 traceback으로 처리 # TODO: 추후 예외처리 로직 추가예정


class HealthConditionService:
    @staticmethod
    async def create_one_condition(
        db: AsyncSession, user_id: int, condition: HealthConditionCreate
    ):
        dict_condition = condition.model_dump()
        # user_id필드 추가
        dict_condition["user_id"] = user_id

        try:
            db_condition = await HealthConditionCrud.create_one_condition_db(
                db, dict_condition
            )
            await db.commit()
            await db.refresh(db_condition)
            return db_condition

        except Exception:
            await db.rollback()
            raise

    # @staticmethod
    # async def create_condition_bulk(
    #     db: AsyncSession, user_id: int, conditions: HealthConditionCreate
    # ):
    #     # conditions input = None이면 db insert 자체를 차단
    #     if not conditions.conditions:
    #         return []

    #     dict_condition
    #     dict_condition = conditions.model_dump()
    #     condition_list = conditions.conditions
    #     dict_conditions = [
    #         {"user_id": user_id, "conditions": con} for con in condition_list
    #     ]
    #     # add user_id from auth context (DB insert용)
    #     # dict_condition["user_id"] = user_id

    #     try:
    #         db_condition_rows = await HealthConditionCrud.create_condition_db(
    #             db, dict_conditions
    #         )   # type(db_condition_rows)= orm obj list

    #         await db.commit()
    #         # await db.refresh(db_condition) # bulk insert 에서 refresh-> err
    #         return db_condition_rows

    #     except Exception:
    #         await db.rollback()
    #         raise

    # read
    @staticmethod
    async def get_condition(db: AsyncSession, user_id: int):
        db_condition = await HealthConditionCrud.get_condition_db(db, user_id)
        if not db_condition:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Found"
            )

        return db_condition

    @staticmethod
    async def delete_condition(db: AsyncSession, user_id: int):
        try:
            await HealthConditionCrud.delete_condition_db(db, user_id)
            await db.commit()
            return True

        except Exception:
            await db.rollback()
            raise

    # @staticmethod
    # async def update_condition(
    #     db: AsyncSession, user_id: int, conditions: HealthConditionUpdate
    # ):
    #     pass
