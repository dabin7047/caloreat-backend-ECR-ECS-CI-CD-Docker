# from fastapi import HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from app.db.models.user_allergy import Allergy
# from app.db.schemas.user_allergy import AllergyCreate, AllergyRead, AllergyUpdate
# from typing import Optional, List


# # 건강 및 식이 제한정보 user_health_conditions
# class AllergyCrud:
#     # create condition
#     @staticmethod
#     async def create_one_allergy_db(db: AsyncSession, allergy: dict):
#         # model_dump (pytdantic-> dict) : service로이동(user_id필드 추가)
#         db_allergy = Allergy(**allergy)
#         db.add(db_allergy)
#         await db.flush()  # PK생성, DB내 query insert
#         return db_allergy

#     # read
#     @staticmethod
#     async def get_allergy_db(db: AsyncSession, user_id: int):
#         result = await db.execute(select(Allergy).where(Allergy.user_id == user_id))
#         return result.scalar_one_or_none()

#     @staticmethod
#     async def update_condition_db():
#         pass

#     @staticmethod
#     async def delete_allergy_db(db: AsyncSession, user_id: int) -> bool:
#         print("input_user_id:", user_id)

#         result = await db.execute(select(Allergy).where(Allergy.user_id == user_id))
#         db_allergy = result.scalar_one_or_none()

#         if not db_allergy:
#             raise HTTPException(status_code=404, detail="Not found")

#         await db.delete(db_allergy)
#         await db.flush()  # db에 쿼리문날림/ 롤백가능
#         return True
