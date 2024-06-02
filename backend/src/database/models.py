from sqlalchemy import Column, Integer, String
from .db import Base

class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True)
	username = Column(String, unique=True)
	hashed_password = Column(String)