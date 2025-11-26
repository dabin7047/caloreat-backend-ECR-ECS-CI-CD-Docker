from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas.user_profile import (
    UserProfileCreate,
    UserProfileRead,
    UserProfileUpdate,
)
from app.db.models.user_profile import UserProfile
from app.db.crud.user_profile import UserProfileCrud

from enum import Enum
from datetime import date
