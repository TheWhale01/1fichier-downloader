from include import *
from auth import get_password_hash

def user_exists(db: Session):
	db_user = db.query(models.User).first()
	if not db_user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such user")
	return db_user

def create_user(db: Session, user: schemas.UserCreate):
	hashed_password: str = get_password_hash(user.password)
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
	db_user = db.query(models.User).filter(models.User.username == username).filter().first()
	return db_user