from include import *

def add_downloads(downloads: list[schemas.DownloadCreate], db: Session = Depends(get_db)):
	db_downloads: list[models.Download] = [models.Download(link=download.link, filename=download.filename, state=download.state, size=download.size, size_unit=download.size_unit, percentage=download.percentage, remaining_time=download.remaining_time) for download in downloads]
	db.bulk_save_objects(db_downloads)
	db.commit()
	return db_downloads

def get_downloads(db: Session = Depends(get_db)):
	return db.query(models.Download).all()

def delete_downloads(db: Session):
	db_downloads = db.query(models.Download).all()
	for db_download in db_downloads:
		db.delete(db_download)
		db.commit()

def update_remaining_time(link: str, remaining_time: int, db: Session = Depends(get_db)):
	db_download = db.query(models.Download).filter(models.Download.link == link).first()
	if db_download is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Could not find download with corresponding link"
		)
	db_download.remaining_time = remaining_time
	db.commit()
	return db_download

def update_dl_state(link: str, state: int, db: Session = Depends(get_db)):
	db_download = db.query(models.Download).filter(models.Download.link == link).first()
	if db_download is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Could not find download with corresponding link"
		)
	db_download.state = state
	db.commit()
	return db_download

def update_dl_percentage(link: str, percentage: float, db: Session = Depends(get_db)):
	db_download = db.query(models.Download).filter(models.Download.link == link).first()
	if db_download is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Could not find download with corresponding link"
		)
	db_download.percentage = percentage
	db.commit()
	return db_download
