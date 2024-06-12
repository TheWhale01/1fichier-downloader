import jwt
import os
import uvicorn
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from passlib.context import CryptContext
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from database.db import get_db, engine
from database.schemas import Token, TokenData, User
from database.models import User
from database import models, schemas