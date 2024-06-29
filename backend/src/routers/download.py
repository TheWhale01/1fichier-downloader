from include import *
from auth import get_current_user
from crud import download as crud_dl
import threading

router = APIRouter(
	prefix='/download'
)

@router.post('')
def add_download_links(links: list[str], user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
	if crud_dl.get_downloads():
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Downloads are already in progress"
		)
	downloader: Downloader = Downloader(links)
	downloads: list[schemas.DownloadCreate] = downloader.init_downloads()
	db_downloads: list[models.Download] = crud_dl.add_downloads(downloads, db)
	dl_worker = threading.Thread(target=downloader.start_downloads())
	dl_worker.start()
	downloader.start_downloads()

@router.get('')
def get_db_downloads(user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
	return {'downloads': crud_dl.get_downloads()}

@router.delete('')
def remove_download_links(db: Session = Depends(get_db)):
	crud_dl.delete_downloads(db)
