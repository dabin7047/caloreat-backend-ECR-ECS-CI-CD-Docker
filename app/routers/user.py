from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db

from app.services.user import register_user,login_user,delete_user,get_user, update_user, read_all_user

from typing import Annotated , List


router = APIRouter(prefix="/users", tags=["User"])

# signup
# login

# logout

# getuser

# delete_user or remove_user

