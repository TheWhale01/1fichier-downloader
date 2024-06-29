from sqlalchemy import Column, Integer, String, Float
from .db import Base

class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True)
	username = Column(String, unique=True)
	hashed_password = Column(String)

class Download(Base):
	__tablename__ = 'download'

	id = Column(Integer, primary_key=True)
	link = Column(Integer, unique=True)
	filename = Column(String, unique=True)
	state = Column(Integer)
	size = Column(Float)
	size_unit = Column(String)
	percentage = Column(Float)
	remaining_time = Column(Integer)
