from sqlalchemy import Column, Integer, String
from .db import Base

class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True)
	username = Column(String, unique=True)
	hashed_password = Column(String)

class Download(Base):
	__tablename__ = 'downlaod'

	# The rest would be sent by the socketio connection
	id = Column(Integer, primary_key=True)
	link = Column(Integer, unique=True)
	filename = Column(String, unique=True)
	state = Column(Integer)