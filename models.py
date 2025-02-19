import uuid
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    lastname = Column(String, index=True)
    age = Column(Integer, index=True)
    email = Column(String, unique=True, index=True)
