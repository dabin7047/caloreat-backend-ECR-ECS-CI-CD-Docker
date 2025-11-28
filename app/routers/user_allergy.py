# from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.core.auth import get_current_user, get_user_id

# from app.db.database import get_db
# from app.db.models.user import User
# from app.db.models.user_allergy import Allergy
# from app.db.schemas.user_allergy import (
#     AllergyCreate,
#     AllergyRead,
#     AllergyUpdate,
# )
# from app.services.user_allergy import AllergyService

# from typing import Annotated, List

# # TODO: Condition/ Allergy endpoint URL path parameter({id}) 추가 고려필요

# router = APIRouter(prefix="/users/me/heatlh-allergies", tags=["Allergy"])


# # create
# @router.post("/", response_model=AllergyRead)
# async def create_allergy_endpoint(
#     allergy: AllergyCreate,
#     current_user: User = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db),
# ):
#     allergy = await AllergyService.create_one_allergy(db, current_user.id, allergy)
#     return allergy


# # read
# @router.get("/", response_model=AllergyRead)
# async def get_allergy_endpoint(
#     current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
# ):
#     user_id = current_user.id
#     db_allergy = await AllergyService.get_allergy(db, user_id)
#     return db_allergy


# # # update
# # @router.patch("/",response_model=AllergyRead)
# # async def update_allergy_endpoint():
# #     pass


# # delete
# # admin api, 권한주입은 따로 함수를구현 후 생성해야함
# @router.delete("/{user_id}")
# async def delete_allergy_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
#     # print("router_uid", user_id)
#     await AllergyService.delete_allergy(db, user_id)

#     return {"deleted": True, "deleted_user_id": {user_id}}


# # delete - allergys, allergy은 oncascade / admin 용
# # TODO: admin 활성화 후 authorization 제한 필요
# # @router.delete("/{allergy_id}", summary="유저컨디션정보 관리")
# # async def delete_allergy_endpoint(
# #     current_user_id: int = Depends(get_user_id), db: AsyncSession = Depends(get_db)
# # ):
# #     await HealthallergyService.delete_allergy(db, current_user_id)
# #     return {"deleted": True, "deleted_user_id": current_user_id}
