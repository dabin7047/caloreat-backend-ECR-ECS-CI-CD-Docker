from fastapi import Request, Response, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.user import UserCrud
from app.db.database import get_db
from app.core.settings import settings
from app.core.jwt_context import verify_token
import jwt


# auth : 요청상태만 책임
# -쿠키없음 / -토큰 유무 / -로그인 옵션 여부 판단 / verify_token 호출
# 1) 인증 쿠키 /  2) 토큰기반 유저확인


# cookies : cookie에서 access_token 꺼내기
# logout 은 router에서 토큰삭제로 대체
def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    # 쿠키가 어떤 상황에서 전송되는지 제어하는 보안기능
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="Lax",  # 동일사이트 요청+최상위 네비게이션 쿠키전송 //oauth 소셜인증 사용시 samesite=secure 필수 : https만 설정가능
        max_age=int(settings.access_token_expire.total_seconds()),
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=int(settings.refresh_token_expire.total_seconds()),
    )


# 인증된 유저인지 여부(Authentication)
# Request 에서 user_id 추출 // source code -> 불필요 중복처리제거
async def get_user_id(request: Request) -> int:
    access_token = request.cookies.get("access_token")
    print("🔥 Received access_token from client:", access_token)
    print(
        "🔥 len(access_token from client):", len(access_token) if access_token else None
    )
    if not access_token:
        raise HTTPException(status_code=401)

    user_id = int(verify_token(access_token))
    print("getuserid:", user_id, type(user_id))
    return user_id


# 로그인한 유저확인(본인 정보확인용도)
async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(request)
    print("currnetUser_id:", user_id)
    # db조회
    current_user = await UserCrud.get_user_by_id(db, user_id)
    if not current_user:
        raise HTTPException(status_code=404, detail="유저 없음")

    return current_user

    # jwt 검증


# token based uesr identification
# #로그인 여부 optional api - 필요시 활성화 후 추가
# async def get_user_id_option(request:Request):
#     access_token=request.cookies.get("access_token")
#     if not access_token:
#         return None
#     try:
#         return verify_token(access_token)
#     except InvalidTokenError:
#         return None
