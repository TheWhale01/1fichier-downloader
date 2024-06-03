from sqlalchemy.orm import Session
from . import models, schemas

def user_exists(db: Session):
	return not(not(db.query(models.User).first()))

def create_user(db: Session, user: schemas.UserCreate):
	hashed_password: str = user.password + "hashed"
	db_user = models.User(username=user.username, hashed_password=hashed_password)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user

def delete_user(db: Session):
	db_user = db.query(models.User).first()
	db.delete(db_user)
	db.commit()

def get_user_by_username(username: str, db: Session):
	db_user = db.query(models.User).filter(models.User.username == username).filter()
	return db_user