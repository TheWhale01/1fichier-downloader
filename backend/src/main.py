from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn
import os
from database import crud, models, schemas
from database.db import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

app = FastAPI()
app.add_middleware(CORSMiddleware,
	allow_origins=['*'],
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*']
)

@app.get('/user')
def get_user(db: Session = Depends(get_db)):
	return {"user": crud.user_exists(db)}

@app.post('/user')
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	return {"user": crud.create_user(db, user)}

@app.delete('/user')
def delete_user(db: Session = Depends(get_db)):
	crud.delete_user(db)
	return {"user": None}

if __name__ == '__main__':
	uvicorn.run("main:app", host=os.getenv("HOST"), port=int(os.getenv("PORT")), reload=True)