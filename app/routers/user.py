from fastapi import APIRouter, Depends, HTTPException, status, Response, Request

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas.user import (
    UserRead,
    UserCreate,
    UserUpdate,
    UserLogin,
    LoginResponse,
)
from app.db.database import get_db
from app.db.models.user import User
from app.services.user import UserService
from app.db.crud.user import UserCrud


from app.core.auth import set_auth_cookies


from typing import Annotated, List

router = APIRouter(prefix="/users", tags=["User"])


# 회원가입 - JWT 로그인 - /me 인증확인 - 수정 - 삭제 - 중복체크
# signup
@router.post("/signup", response_model=UserRead)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    db_user = await UserService.register_user(
        db, user.email, user.username, user.password
    )
    return db_user


# login ( 유저정보만 클라이언트로 반환)
@router.post("/login", response_model=LoginResponse)
async def login(
    user: UserLogin, response: Response, db: AsyncSession = Depends(get_db)
):  # response fastapi가 자동으로 dependency 주입
    result = await UserService.login(db, user)
    db_user, access_token, refresh_token = result
    set_auth_cookies(
        response, access_token, refresh_token
    )  # token은 body x 쿠키로 관리(localstorage 필요 x)/ CSRF 취약점 존재
    return db_user


# 사용자 조회 (본인 정보조회)
@router.get("/me", response_model=UserRead)
async def get_authenticated_user():
    return None


# # 모든 사용자조회(관리자용)
# @router.get("/", response_model=List[UserRead])
# async def read_all_user_route(db: AsyncSession, current_user: ):
#     users = await read_all_user(db)
#     return users


# logout

# # # delete_user
# @router.delete("/delete/{user_id}")
# async def delete_user(user_id:int,
#                       db:AsyncSession=Depends(get_db)):
#     result = await UserCrud.delete_user_by_id(user_id,db)
#     return {"msg":"회원삭제","deleted":result}
# # user update
# # @router.put("/update/{user_id}")
# # async def update_user_by_id(user:UserUpdate,
# #                             user_id:int,
# #                             db:AsyncSession=Depends(get_db)):
# #     result = await UserCrud.update_user_by_id(user,user_id,db)
# #     return result

# fastapi oauth2pwbearer방식(header) 병행 or 프론트에서 토큰이 필요할 시 사용(모바일앱 염두)
# # # login
# # @router.post("/login", response_model=UserLogin)
# # async def login(user:UserLogin, response:Response,db:AsyncSession=Depends(get_db)) -> AuthResponse:
# #     result = await UserService.login(user,db)
# #     verified_staff, access_token, refresh_token = result
# #     set_auth_cookies(response, access_token, refresh_token)
# #     return AuthResponse(verified_staff=verified_staff ,access_token=access_token, refresh_token=refresh_token)


# logout
async def logout(request: Request, response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return True
