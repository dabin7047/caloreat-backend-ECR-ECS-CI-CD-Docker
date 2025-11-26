from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, Annotated
from enum import Enum

# 건강 및 식이 제한정보 user_health_conditions
# 질병정보등은 선택사항
# 유저정보


# base
class HealthConditionBase(BaseModel):
    condition_code: str
    condition_type: str | None = None  # TODO: conditino 선택시에만 선택되게
    # allergy는 건강유의사항과 속성이다름 -> ㅇ

    # severity: str | None = None


# request
# condition은 optional 필수 생성필드가 아니므로 create의 의미가 x


# create
# class HealthConditionCreate(HealthConditionBase):
#     pass


# update
class HealthConditionUpdate(HealthConditionBase):
    pass


# response
# read
class HealthConditionInDB(HealthConditionBase):
    id: int  # TODO: alias 적용 condition_id
    user_id: int

    class Config:
        from_attributes = True


class HealthConditionRead(HealthConditionInDB):
    pass
