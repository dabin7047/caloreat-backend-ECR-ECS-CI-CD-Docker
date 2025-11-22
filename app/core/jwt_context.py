from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, status

from app.core.settings import settings
import uuid

# passlib:해싱,검증, bcrypt: 내부 알고리즘
pwd_context = CryptContext(schemes=["bcrypt"])


# 1) 비밀번호 해싱
# 해시값 저장 async 필요x
def get_pwd_hash(password: str) -> str:
    return pwd_context.hash(password)


# verify password
def verify_pwd(plain_password: str, hashed_pasword: str):
    return pwd_context.verify(plain_password, hashed_pasword)


# --------------------------------


# 2) 토큰 생성
# 공통 JWT 생성기       // uid =sub(subject) 토큰의주인,주체 // sub=DB PK(1,2,3...)
def create_token(sub: int, expires_delta: timedelta, **kwargs) -> str:
    print("TOKEN CREATE KEY:", settings.secret_key)
    expire = datetime.now(timezone.utc) + expires_delta
    # payload 변수로 혼동방지   //troubleshooting : expire.timestamp -> float -> int(expire.timestamp)
    payload = {"exp": int(expire.timestamp()), "sub": str(sub)}
    payload.update(kwargs)  # kwargs- refresh token- jti :(random uuid)
    encoded_jwt = jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algo)
    return encoded_jwt


# access_token 15min - API 인증용
def create_access_token(sub: int) -> str:
    return create_token(sub=sub, expires_delta=settings.access_token_expire)


# refresh_token 7days - access재발급 + jti 포함
def create_refresh_token(sub: int) -> str:
    return create_token(
        sub=sub, jti=str(uuid.uuid4()), expires_delta=settings.refresh_token_expire
    )  # jti refresh token JWT ID : 토큰 자체의 고유 식별자, user logout시 refreshtoken 폐기 (Refresh Token Rotation)


# -----------------------------


# 3) 토큰 검증(token verification)
# decode: JWT str -> dict(payload) // PyJWT가 서명검증+ exp검증 수행
def decode_token(token: str) -> dict:
    print("TOKEN DECODE KEY:", settings.secret_key)
    print("settings.jwt_algo =", settings.jwt_algo, repr(settings.jwt_algo))
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algo])
        return payload
    except Exception as e:
        print("🔥 JWT DECODE ERROR:", type(e).__name__, str(e))
        raise


# verify_token
# + 예외처리 auth예외처리 제외 verify_token에서 일괄 관리
def verify_token(token: str):
    print("RAW TOKEN BYTES:", list(token.encode()))
    try:
        payload = decode_token(token)

    # expire 만료되었는가?
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰 만료"
        )

    # 토큰이 진짜인가? (잘못된서명, 변조, 구조오류, decode실패시)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 토큰"
        )

    # sub(uid) 유저정보가 없을시
    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=401, detail="토큰 데이터가 올바르지 않습니다")

    return sub
