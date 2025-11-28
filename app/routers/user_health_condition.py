from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user, get_user_id
from app.core.auth import set_login_cookies, set_access_cookie

from app.db.database import get_db
from app.db.models.user import User
from app.db.models.user_health_condition import HealthCondition
from app.db.schemas.user_health_condition import (
    HealthConditionCreate,
    HealthConditionRead,
    HealthConditionUpdate,
)
from app.services.user_health_condition import HealthConditionService

from typing import Annotated, List


router = APIRouter(prefix="/users/me/heatlh-conditions", tags=["HealthCondition"])


# one conditoin
@router.post("/", response_model=HealthConditionRead)
async def create_condition_endpoint(
    conditions: HealthConditionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    row = await HealthConditionService.create_one_condition(
        db, current_user.id, conditions
    )
    return row


# # add conditions
# @router.post("/", response_model=List[HealthConditionRead])
# async def create_condition_list_endpoint(
#     conditions: HealthConditionCreate,
#     current_user: User = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db),
# ):
#     user_id = current_user.id
#     new_profile = await HealthConditionService.create_one_condition(db, user_id, conditions)
#     return new_profile


# read one_condition
@router.get("/", response_model=HealthConditionRead)
async def get_condition_endpoint(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    user_id = current_user.id
    db_condition = await HealthConditionService.get_condition(db, user_id)
    return db_condition


# read_all_conditions

# # update conditions
# @router.patch("/", response_model=HealthConditionRead, summary="건강정보 수정")
# async def update_condition_endpoint(
#     conditions: HealthConditionUpdate,
#     current_user: User = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db),
# ):
#     user_id = current_user.id
#     db_condition = await HealthConditionService.update_condition(
#         db, user_id, conditions
#     )
#     return db_condition


#
# admin api, 권한주입은 따로 함수를구현 후 생성해야함
@router.delete("/{user_id}")
async def delete_condition_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    await HealthConditionService.delete_condition(db, user_id)
    return {"deleted": True, "deleted_user_id": {user_id}}


# delete - conditions, condition은 oncascade / admin 용
# TODO: admin 활성화 후 authorization 제한 필요
# @router.delete("/{condition_id}", summary="유저컨디션정보 관리")
# async def delete_condition_endpoint(
#     current_user_id: int = Depends(get_user_id), db: AsyncSession = Depends(get_db)
# ):
#     await HealthConditionService.delete_condition(db, current_user_id)
#     return {"deleted": True, "deleted_user_id": current_user_id}
