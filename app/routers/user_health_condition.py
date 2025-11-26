from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user, get_user_id
from app.core.auth import set_login_cookies, set_access_cookie

from app.db.database import get_db
from app.db.models.user_health_condition import HealthCondition
from app.db.schemas.user_health_condition import (
    HealthConditionCreate,
    HealthConditionRead,
    HealthConditionUpdate,
)
from app.services.user_health_condition import HealthConditionService

from typing import Annotated, List


router = APIRouter(prefix="user/me/heatlh-conditions", tags=["HealthCondition"])


# POST /users/me/health-conditions
@router.post("/", response_model=HealthConditionRead)
async def create_condition_endpoint(
    condition: HealthConditionCreate, db: AsyncSession = Depends(get_db)
):
    pass


@router.get("/", response_model=HealthConditionRead)
async def get_condition_endpoint(db: AsyncSession = Depends(get_db)):
    pass


@router.patch("/", response_model=HealthConditionRead)
async def update_condition_endpoint(
    condition: HealthConditionUpdate, db: AsyncSession = Depends(get_db)
):
    pass


# delete - profile, condition은 oncascade / admin 용
# TODO: admin 활성화 후 authorization 제한 필요
@router.delete("/{condition_id}", summary="유저컨디션정보 관리")
async def delete_condition_endpoint(
    current_user_id: int = Depends(get_user_id), db: AsyncSession = Depends(get_db)
):
    await HealthConditionService.delete_condition(db, current_user_id)
    return {"deleted": True, "deleted_user_id": current_user_id}
