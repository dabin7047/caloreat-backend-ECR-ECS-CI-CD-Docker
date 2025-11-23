from app.db.database import Base
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Annotated

# 건강 및 식이 제한정보 user_health_conditions


class HealthConditionBase(BaseModel):
    pass
