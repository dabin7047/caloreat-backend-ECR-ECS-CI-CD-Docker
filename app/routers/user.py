from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
# from app.db.database import get_db



from typing import Annotated , List


router = APIRouter(prefix="/users", tags=["User"])


@router.get("/test")
async def router_test():
    return {"msg":"Hello, AIvocado!"}
# signup

# login

# logout

# getuser

# delete_user or remove_user

