from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user, get_user_id
from app.core.auth import set_login_cookies, set_access_cookie

from app.db.database import get_db
from app.db.models.user import User
from app.db.crud.user import UserCrud

from app.services.user import UserService

from typing import Annotated, List

# URL path 언더스코어 금지원칙 user_profile -> user-profile
router = APIRouter(prefix="/user-profiles", tags=["UserProfile"])

# GET /users/me/profile – 프로필 하나 조회

# PATCH /users/me/profile – 특정 필드만 수정
