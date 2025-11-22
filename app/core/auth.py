from fastapi import Request, Response, HTTPException, Depends, status

# from jwt import ExpiredSignatureError, InvalidTokenError
from app.core.settings import settings
from app.core.jwt_context import verify_pwd
from typing import Optional
import uuid
from fastapi.security import OAuth2PasswordBearer

# auth : 요청상태만 책임
# -쿠키없음 / -토큰 유무 / -로그인 옵션 여부 판단 / verify_token 호출


# cookies
def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    # 쿠키가 어떤 상황에서 전송되는지 제어하는 보안기능
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="Lax",  # 동일사이트 요청+최상위 네비게이션 쿠키전송 //oauth 외부요청 사용시 samesite=secure 필수 : https만 설정가능
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


# 요청객체에서 access_token꺼내서
# 현재 로그인한 사용자 id가져오기 위해
async def get_user_id(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401)

    try:
        user_id = verify_token(access_token)
        if user_id is None:
            raise HTTPException(status_code=401)
        return user_id
    except InvalidTokenError:
        raise HTTPException(status_code=401)


# Oauth dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 현재 사용자 정보 추출 및 검증
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


# #로그인 여부 optional apii
# async def get_user_id_option(request:Request):
#     access_token=request.cookies.get("access_token")
#     if not access_token:
#         return None
#     try:
#         return verify_token(access_token)
#     except InvalidTokenError:
#         return None
