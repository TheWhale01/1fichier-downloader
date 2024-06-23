from include import *
from auth import get_current_user
from crud import download as crud_dl

router = APIRouter(
	prefix='/download'
)

@router.post('')
def add_download_links(links: list[str], user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
	downloader: Downloader = Downloader(links)
	downloads: list[schemas.DownloadCreate] = downloader.init_downloads()
	db_downloads: list[models.Download] = crud_dl.add_downloads(downloads, db)
	return {'downloads': db_downloads}
