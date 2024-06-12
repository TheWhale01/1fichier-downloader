from include import *
import auth
from routers import user, download

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
app.include_router(download.router)

if __name__ == '__main__':
	uvicorn.run("main:app", host=os.getenv("HOST"), port=int(os.getenv("PORT")), reload=True)