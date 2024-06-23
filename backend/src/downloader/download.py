import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from sqlalchemy.sql.compiler import crud
from include import *
from crud import download

class File:
    def __init__(self, filename: str, size: float, size_unit: str):
        self.filename: str = filename
        self.size: float = size
        self.size_unit: str = size_unit

class	Downloader:
	def	__init__(self, links: list[str]):
		self.links:	list[str] = links
		self.browser: WebDriver = None
		self.download_path: str | None = os.getenv('DOWNLOAD_PATH')
		self.wait_time: int = 2
		self.init_browser()

	def	__del__(self):
		self.close_browser()

	def	init_browser(self):
		options = webdriver.FirefoxOptions()
		options.add_argument('--headless')
		self.browser = webdriver.Firefox(options=options)
		self.browser.set_window_position(0, 0)
		self.browser.set_window_size(1920, 1080)
		self.browser.install_addon(os.path.abspath('./downloader/extensions/ublock_origin-1.52.2.xpi'))

	def	close_browser(self):
	   self.browser.close()

	def remove_popups(self):
		try:
			cookie_box = self.browser.find_element(By.CSS_SELECTOR, '.cookie_box_close')
			cookie_box.click()
		except:
			pass
		close_ad_btn = self.browser.find_element(By.CSS_SELECTOR, "button.ui-button")
		close_ad_btn.click()

	def get_file_info(self) -> File:
		filename_el = self.browser.find_element(By.XPATH, '/html/body/form/table/tbody/tr[1]/td[3]')
		size_el = self.browser.find_element(By.XPATH, '/html/body/form/table/tbody/tr[3]/td[2]')
		filename: str = filename_el.get_attribute('innerHTML')
		size_group: str = size_el.get_attribute('innerHTML').split()
		return File(filename=filename, size=float(size_group[0]), size_unit=size_group[1])

	def	init_downloads(self) -> list[schemas.DownloadCreate]:
		db_downloads: list[schemas.DownloadCreate] = []
		for	link in	self.links:
			self.browser.get(link)
			sleep(self.wait_time)
			self.remove_popups()
			file: File = self.get_file_info()
			download = schemas.DownloadCreate(link=link, filename=file.filename, state=State.waiting, size=file.size, size_unit=file.size_unit)
			db_downloads.append(download)
		return db_downloads

def main():
	downloader: Downloader = Downloader(["https://1fichier.com/?kjv5bsxrhjs5047b8yv8&af=3697663"])
	downloader.init_downloads()

if __name__ == "__main__":
	main()
