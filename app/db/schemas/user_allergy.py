# from pydantic import BaseModel, Field
# from datetime import datetime, date
# from typing import Optional, Annotated


# # user_allergies


# # base
# class AllergyBase(BaseModel):
#     allergy: str


# # create
# class AllergyCreate(AllergyBase):
#     pass


# # update
# class AllergyUpdate(AllergyCreate):
#     pass


# # response
# # read
# class AllergyInDB(AllergyBase):
#     allregy_id: int = Field(..., alias="id")  # alias 적용 allergy_id

#     # created_at: datetime  # 기간별 상태변화 추적필요하면 활성화
#     pass
#     # updated_at:

#     class Config:
#         from_attributes = True


# class AllergyRead(AllergyInDB):
#     pass
