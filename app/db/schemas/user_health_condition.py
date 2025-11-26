from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, Annotated
from enum import Enum

# 건강 및 식이 제한정보 user_health_conditions
# 질병정보등은 선택사항
# 유저: condition = 1:n
# 향후 ai 학습or 추론 고려 개별 endpoints작성


# base
class HealthConditionBase(BaseModel):
    """
    conditions: 중복선택가능
    임시 condition codes:
    "high_blood_pressure"
    "low_blood_pressure"
    "diabetes"
    "thyroid_low"
    "thyroid_high"
    """

    conditions: list[str]
    # TODO: 나중에 nutri 정보기반 학습, 통계시에는 mapping or 칼럼명 필요할수도 있음
    # condition_type: str | None = None
    # allergy는 건강유의사항과 속성이다름 -> ㅇ

    # severity: str | None = None


# request client가 보내는 필드
# condition은 optional 필수 생성필드가 아니므로 create의 의미가 x


# create
class HealthConditionCreate(HealthConditionBase):
    pass


# update
class HealthConditionUpdate(HealthConditionBase):
    pass


# response
# read
class HealthConditionInDB(HealthConditionBase):
    id: int  # TODO: alias 적용 condition_id
    created_at: datetime
    # updated_at:

    class Config:
        from_attributes = True


class HealthConditionRead(HealthConditionInDB):
    pass
