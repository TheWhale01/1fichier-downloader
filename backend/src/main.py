from fastapi import FastAPI
import uvicorn
import os
from database import models
from database.db import engine
from fastapi.middleware.cors import CORSMiddleware
from routers import user
import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(CORSMiddleware,
	allow_origins=['*'],
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*']
)

app.include_router(user.router)
app.include_router(auth.router)

if __name__ == '__main__':
	uvicorn.run("main:app", host=os.getenv("HOST"), port=int(os.getenv("PORT")), reload=True)