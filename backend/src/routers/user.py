from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import crud, schemas
from database.db import get_db
from typing import Annotated
from auth import oauth2_scheme
from database.schemas import User
from database import crud
from auth import get_current_user

router = APIRouter(
	prefix='/user'
)

@router.get('')
def get_user(db: Session = Depends(get_db)):
	return {"user": crud.user_exists(db)}

@router.get('/me')
def get_me(current_user: Annotated[User, Depends(get_current_user)]):
	return {'user': current_user}

@router.post('')
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	return {"user": crud.create_user(db, user)}

@router.delete('')
def delete_user(db: Session = Depends(get_db)):
	crud.delete_user(db)
	return {"user": None}

