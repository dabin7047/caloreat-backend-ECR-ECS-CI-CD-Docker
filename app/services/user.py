from fastapi import HTTPException, status
from app.db.schemas.user import UserCreate, UserUpdate, UserLogin
from app.core.jwt_context import (
    get_pwd_hash,
    verify_pwd,
    create_access_token,
    create_refresh_token,
)

# from app.core.security import hash_password # security.py 파일 만든뒤 활성화
from app.db.models.user import User
from app.db.crud.user import UserCrud


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

# from app.core.jwt_context import get_pwd_hash

from datetime import datetime


# Service = Business Logic


class UserService:
    # 회원가입 (비밀번호 해시 후 저장)

    # create
    @staticmethod
    async def register_user(db: AsyncSession, email: str, username: str, password: str):
        # 중복 이메일 체크
        existing_email = await UserCrud.get_user_by_email(db, email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용중인 이메일입니다",
            )

        # 중복 username 체크
        existing_username = await UserCrud.get_user_by_username(db, username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용중인 이름입니다",
            )

        # password hasing
        hashed_pw = get_pwd_hash(password)
        user_create = UserCreate(email=email, username=username, password=hashed_pw)

        return await UserCrud.create_user(db, user_create)

    # read user by id
    # id기준으로 사용자 프로필조회 ≠ 이메일기준으로 로그인전용 함수
    @staticmethod
    async def get_user(db: AsyncSession, user_id: str):
        user = await UserCrud.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User Not Found"
            )
        return user

    # read userlist (관리자)
    @staticmethod
    async def read_all_user(db: AsyncSession):
        users = await UserCrud.get_all_user(db)
        return users

    # update (updated_at 추가 고려)
    @staticmethod
    async def update_user(db: AsyncSession, current_user_id: int, user: UserUpdate):
        # db 유효성 검사
        db_user = await UserCrud.get_user_by_id(db, current_user_id)
        if not db_user:
            raise HTTPException(404, "Not found")

            # patch(요청에서 전달된 필드만 업데이트하겠다) {"email":"aa@naver.com"}
        update_user = user.model_dump(exclude_unset=True)

        if user.password:
            update_user["password"] = get_pwd_hash(user.password)

        #
        updated_user = await UserCrud.update_user(db, db_user, update_user)

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id not Found",
            )

        return updated_user

    # delete
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        try:
            await UserCrud.delete_user_by_id(db, user_id)
            await db.commit()
            return True

        except Exception:
            await db.rollback()
            raise

    # login
    @staticmethod
    async def login(db: AsyncSession, user: UserLogin) -> tuple:
        # username, email 둘다 허용하려면
        account = user.account

        # 이메일, 아이디 허용분기
        if "@" in account and "." in account:
            db_user = await UserCrud.get_user_by_email(db, account)  # login용 email조회
        else:
            db_user = await UserCrud.get_user_by_username(db, account)

        if not db_user or not verify_pwd(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비밀번호")

        # token
        access_token = create_access_token(db_user.id)
        refresh_token = create_refresh_token(db_user.id)
        print("len(access_token):", len(access_token))
        print("len(refresh_token):", len(refresh_token))

        return db_user, access_token, refresh_token

        # # refresh_token rotation 추가시 활성화(미들웨어사용 토큰 자동갱신)
        # updated_user = await UserCrud.update_refresh_token_id(
        #     db, db_user.user_id, refresh_token
        # )
        # await db.commit() 로그인과정에서 뭔가를DB에 변경 했을때만필요(refresh_token rotation)
        # await db.refresh(db_user)
