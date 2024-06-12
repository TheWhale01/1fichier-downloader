from include import *
from auth import get_current_user
from crud import user as user_service

router = APIRouter(
	prefix='/user'
)

@router.get('')
def get_user(db: Session = Depends(get_db)):
	return {"user": user_service.user_exists(db)}

@router.get('/me')
def get_me(current_user: Annotated[User, Depends(get_current_user)]):
	return {'user': current_user}

@router.post('')
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	return {"user": user_service.create_user(db, user)}

@router.delete('')
def delete_user(db: Session = Depends(get_db)):
	user_service.delete_user(db)
	return {"user": None}

