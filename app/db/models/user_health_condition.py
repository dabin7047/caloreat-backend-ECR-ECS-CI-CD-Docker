from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


# 건강 및 식이 제한정보 user_health_conditions
class HealthCondition(Base):
    __tablename__ = "user_health_conditions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    condition_name = Column(String(100), nullable=True)
    condition_type = Column(String(50), nullable=True)  # disease, allergy, ..
    severity = Column(String(10), nullable=True)  # low/ medium / high

    user = relationship("User", back_populates="condition")

    # activity_level = Column(Integer, nullable=True) # 운동량(하루활동량)
