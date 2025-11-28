# from fastapi import HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.db.schemas.user_allergy import AllergyCreate, AllergyRead

# from app.db.models.user_allergy import Allergy
# from app.db.crud.user_allergy import AllergyCrud

# from enum import Enum
# from datetime import date


# class AllergyService:
#     @staticmethod
#     async def create_one_allergy(
#         db: AsyncSession, user_id: int, allergy: AllergyCreate
#     ):
#         dict_allergy = allergy.model_dump()
#         # user_id필드 추가
#         dict_allergy["user_id"] = user_id

#         try:
#             db_allergy = await AllergyCrud.create_one_allergy_db(db, dict_allergy)
#             await db.commit()
#             await db.refresh(db_allergy)
#             return db_allergy

#         except Exception:
#             await db.rollback()
#             raise

#     # read
#     @staticmethod
#     async def get_allergy(db: AsyncSession, user_id: int):
#         db_allergy = await AllergyCrud.get_allergy_db(db, user_id)
#         if not db_allergy:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Found"
#             )

#         return db_allergy

#     # update
#     @staticmethod
#     async def update_allergy(db: AsyncSession, user_id: int, allergies):
#         pass

#     # delete
#     @staticmethod
#     async def delete_allergy(db: AsyncSession, user_id: int):
#         print("service_uid:", user_id)
#         try:
#             await AllergyCrud.delete_allergy_db(db, user_id)
#             await db.commit()
#             return True

#         except Exception:
#             await db.rollback()
#             raise
