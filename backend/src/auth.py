from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from database import crud
from database.db import get_db
from database.schemas import Token, TokenData
from database.models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
# from jwt.exceptions import InvalidTokenError
from datetime import timedelta, datetime
import jwt
import os

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
router = APIRouter()

def verify_password(plain_password: str, hashed_password: str) -> bool:
     return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
     return pwd_context.hash(password)

def auth_user(db: Session, username: str, password: str) -> User:
    user: User = crud.get_user_by_username(username, db)
    if not user:
        return
    if not verify_password(password, user.hashed_password):
        return
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> dict:
    to_encode: dict = data.copy()
    if expires_delta:
        expire: timedelta = datetime.now() + expires_delta
    else:
        expire: timedelta = datetime.now() + timedelta(minutes=int(os.getenv('TOKEN_EXPIRE')))
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv('ALGORITHM'))
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> User:
    creds_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )	
    try:
        paylaod = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        username: str = paylaod.get('sub')
        if username is None:
            raise creds_exception
        token_data = TokenData(username=username)
    except:
        raise creds_exception
    user = crud.get_user_by_username(username=token_data.username, db=db)
    if user is None:
        raise creds_exception
    return user

@router.post('/token')
def login(data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    user: User = auth_user(db=db, username=data.username, password=data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token_expires = timedelta(minutes=int(os.getenv('TOKEN_EXPIRE')))
    access_token = create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type='bearer')