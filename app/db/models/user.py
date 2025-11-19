from sqlalchemy import Column, Integer, String,ForeignKey
from app.db.database import Base 

#서버구동 test table (임시)
class User(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True,  nullable=False)
    password = Column(String(255), nullable=False) 