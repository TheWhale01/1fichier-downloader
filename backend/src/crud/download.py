from include import *

def add_downloads(downloads: list[schemas.DownloadCreate], db: Session = Depends(get_db)):
	db_downloads: list[models.Download] = [models.Download(link=download.link, filename=download.filename, state=download.state, size=download.size, size_unit=download.size_unit) for download in downloads]
	db.bulk_save_objects(db_downloads)
	db.commit()
	return db_downloads

def delete_downloads(db: Session):
	db_downloads = db.query(models.Download).all()
	for db_download in db_downloads:
		db.delete(db_download)
		db.commit()
