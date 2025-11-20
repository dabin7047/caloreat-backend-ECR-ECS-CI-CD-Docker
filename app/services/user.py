from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.db.crud.user import UserCrud
from app.db.schemas.user import UserCreate, UserUpdate
from app.core.jwt_context import get_pwd_hash

from datetime import datetime

class UserService: 
    #DB에서 해당 id의 사용자 조회 
    @staticmethod
    async def get_user(db:AsyncSession, user_id:int):
        db_user=await UserCrud.get_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="사용자 찾을 수 없다")
        return db_user

    #회원가입  
    # user create 
    @staticmethod
    async def signup(db:AsyncSession, user:UserCreate):
        #중복 username확인
        if await UserCrud.get_username(db, user.username):
            raise HTTPException(status_code=400,  detail="이미 사용중인 이름이다")
        
        #username없으면 -> username, password, email을 디비에 저장
        hash_pw=await get_pwd_hash(user.password) #비번 해싱
        user_create=UserCreate(username=user.username, password=hash_pw, email=user.email)

        try:
            db_user=await UserCrud.create(db,user_create)
            await db.commit()
            await db.refresh(db_user)
            return db_user
        
        except Exception:
            raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비번이다")
        
    # user delete
    async def delete_user(db: AsyncSession, user_id: int):
        is_deleted = await UserCrud.delete_user(db, user_id)
        if not is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found."
            )
        return {"message": "User deleted successfully"}
    
    #user update    
    async def update_user(db: AsyncSession, user_id: int ,user_data:UserUpdate):
        hash_pw = None
        if user_data.password:
            hash_pw = get_pwd_hash(user_data.password)

        updated_user = await UserCrud.update_user(
            db,
            user_id=user_id,
            user_name=user_data.username,
            email=user_data.email,
            hash_pw=hash_pw
        )

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not Found"
            )

        return updated_user  


    # User Login
    # # Login
    # @staticmethod
    # async def login(db: AsyncSession, user: UserLogin) -> tuple:
    #     db_user = await UserCrud.get_email(db, user.email)
    #     if not db_user or not await verify_pwd(user.password, db_user.password):
    #         raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비밀번호")
        

    #     refresh_token = create_refresh_token(db_user.user_id)
    #     access_token = create_access_token(db_user.user_id)

    #     updated_user = await UserCrud.update_refresh_token_id(db, db_user.user_id, refresh_token)
    #     await db.commit()
    #     await db.refresh(updated_user)

    #     return updated_user, access_token, refresh_token

    # version
    # login  (username: phone, password:password 사용) / 
  
    # @staticmethod
    # async def login(user:UserLogin, db:AsyncSession)-> tuple[User,str,str]:
    #     db_user = await UserCrud.get_phone(user.phone,db)        

        
    #     #jwt token 
    #     access_token = create_access_token(db_user.user_id)   
    #     refresh_token = create_refresh_token(db_user.user_id)

    #     verified_staff= await UserCrud.update_refresh_token(db_user.user_id,
    #                                                         refresh_token,db)
    #     await db.commit()
    #     await db.refresh(verified_staff)
    #     return verified_staff, access_token, refresh_token

