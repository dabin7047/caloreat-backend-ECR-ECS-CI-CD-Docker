from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


# 건강 및 식이 제한정보 user_health_conditions
class HealthCondition(Base):
    __tablename__ = "user_health_conditions"

    id: int = Column()
