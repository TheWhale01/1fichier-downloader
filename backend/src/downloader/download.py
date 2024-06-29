from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from sqlalchemy.sql.compiler import crud
from include import *
from crud import download as crud_dl
import requests

class File:
	def __init__(self, filename: str, size: float, size_unit: str) -> None:
		self.filename: str = filename
		self.size: float = size
		self.size_unit: str = size_unit


class	Downloader:
	class BrowserNotInitiated(Exception):
		def __init__(self) -> None:
			super().__init__('Webdriver is not initiated.')

	class NoDownloadLink(Exception):
		def __init__(self) -> None:
			super().__init__('No download link found.')

	def get_size_multiplier(self, unit: str) -> int:
		if unit == 'Go':
			return 1073741824
		elif unit == 'Mo':
			return 1048576
		return 1

	def	__init__(self, links: list[str], extension_path: str = './src/downloader/extensions/ublock_origin-1.52.2.xpi', download_path: str | None = os.getenv('DOWNLOAD_PATH')) -> None:
		self.links:	list[str] = links
		self.extension_path: str = extension_path
		self.browser: WebDriver = None
		if download_path is None:
			self.download_path: str = '/downloads/'
		else:
			self.download_path: str = download_path
		self.wait_time: int = 2
		self.db_downloads: list[schemas.DownloadCreate] = []
		self.init_browser()

	def	__del__(self) -> None:
		self.close_browser()

	def	init_browser(self) -> None:
		options = webdriver.FirefoxOptions()
		# options.add_argument('--headless')
		self.browser = webdriver.Firefox(options=options)
		self.browser.set_window_position(0, 0)
		self.browser.set_window_size(1920, 1080)
		self.browser.install_addon(os.path.abspath(self.extension_path))

	def	close_browser(self) -> None:
		if self.browser is None:
			raise self.BrowserNotInitiated()
		self.browser.close()
		self.browser = None

	def remove_popups(self) -> None:
		try:
			cookie_box = self.browser.find_element(By.CSS_SELECTOR, '.cookie_box_close')
			cookie_box.click()
		except:
			pass
		try:
			close_ad_btn = self.browser.find_element(By.CSS_SELECTOR, "button.ui-button")
			close_ad_btn.click()
		except:
			pass

	def get_file_info(self) -> File:
		filename_el = self.browser.find_element(By.XPATH, '/html/body/form/table/tbody/tr[1]/td[3]')
		size_el = self.browser.find_element(By.XPATH, '/html/body/form/table/tbody/tr[3]/td[2]')
		filename: str | None = filename_el.get_attribute('innerHTML')
		size_group_str: str | None = size_el.get_attribute('innerHTML')
		if filename is None or size_group_str is None:
			raise Exception("Could not get file informations")
		size_group: list[str] = size_group_str.split()
		return File(filename=filename, size=float(size_group[0]), size_unit=size_group[1])

	def	init_downloads(self) -> list[schemas.DownloadCreate]:
		for	link in	self.links:
			self.browser.get(link)
			sleep(self.wait_time)
			self.remove_popups()
			file: File = self.get_file_info()
			download = schemas.DownloadCreate(
				link=link,
				filename=file.filename,
				state=State.waiting,
				size=file.size,
				size_unit=file.size_unit,
				percentage=0,
				remaining_time=0
			)
			self.db_downloads.append(download)
		crud_dl.add_downloads(self.db_downloads)
		self.browser.close()
		return self.db_downloads

	def get_waiting_time(self) -> int:
		wait_time_el: WebElement | None = None
		try:
			wait_time_el = self.browser.find_element(By.CSS_SELECTOR, "div.ct_warn:nth-child(3)")
		except:
			return 0
		if wait_time_el is None:
			return 0
		wait_time_str: str= wait_time_el.text.split('\n')[2]
		wait_time_str = wait_time_str.replace('Vous devez attendre encore ', '')
		wait_time_str = wait_time_str.replace(' minutes.', '')
		wait_time: int = int(wait_time_str)
		return wait_time * 60

	def download_link(self, db_download: schemas.DownloadCreate, dl_link: str) -> None:
		filepath: str = os.path.join(self.download_path, db_download.filename)
		with open(filepath, 'wb') as file:
			crud_dl.update_dl_state(db_download.link, State.downloading)
			response = requests.get(dl_link, stream=True)
			for chunk in response.iter_content(1024):
				if chunk is None:
					break
				db_download.percentage = 100 * (file.tell() / self.get_size_multiplier(db_download.size_unit)) / db_download.size
				print(f'{db_download.percentage}%')
				file.write(chunk)
		db_download.state = State.done

	def get_dl_link(self) -> str:
		access_dl_btn: WebElement = self.browser.find_element(By.ID, "dlb")
		access_dl_btn.click()
		sleep(self.wait_time)
		dl_btn: WebElement = self.browser.find_element(By.CSS_SELECTOR, ".ok")
		dl_link: str | None = dl_btn.get_attribute("href")
		if not dl_link:
			raise self.NoDownloadLink()
		return dl_link

	def start_downloads(self) -> None:
		if len(self.db_downloads) == 0:
			return
		for db_download in self.db_downloads:
			self.init_browser()
			self.browser.get(db_download.link)
			self.remove_popups()
			sleep(self.wait_time)
			time_before_next_dl: int = self.get_waiting_time()
			if time_before_next_dl:
				self.close_browser()
				crud_dl.update_dl_state(db_download.link, State.waiting)
				crud_dl.update_dl_state(db_download.link, time_before_next_dl)
				sleep(time_before_next_dl)
				self.init_browser()
				self.browser.get(db_download.link)
				sleep(self.wait_time)
				self.remove_popups()
			dl_link: str = self.get_dl_link()
			self.close_browser()
			self.download_link(db_download, dl_link)
			db_download.state = State.downloading;

def main():
	downloader: Downloader = Downloader(["https://1fichier.com/?kjv5bsxrhjs5047b8yv8&af=3697663"], extension_path='/home/whale/Documents/Codes/Svelte/1fichier-downloader/backend/src/downloader/extensions/ublock_origin-1.58.0.xpi')
	downloader.init_downloads()
	downloader.start_downloads()

if __name__ == "__main__":
	main()
