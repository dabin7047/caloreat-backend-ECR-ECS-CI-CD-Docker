from fastapi import Request, Response, HTTPException
from jwt import ExpiredSignatureError, InvalidTokenError
from app.core.settings import settings
from app.core.jwt_context import verify_token
from typing import Optional

#cookies
def set_auth_cookies():
    pass
    #access token
    #refresh token

#oauth2_scheme
#db_dependencty (opt.)
