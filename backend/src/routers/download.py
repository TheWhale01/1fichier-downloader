from fastapi import APIRouter, Depends
from typing import Annotated
from database.schemas import User
from auth import get_current_user

router = APIRouter(
	prefix='/download'
)

@router.post('')
def add_download_links(links: list[str], user: Annotated[User, Depends(get_current_user)]):
	print(links)