from sqlalchemy import Column, Integer, String,ForeignKey,DateTime, func
from app.db.database import Base, declarative_base


#서버구동 test table (임시)



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
