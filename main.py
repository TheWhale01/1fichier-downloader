from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
import shutil
import datetime
import requests
from tqdm import tqdm
import argparse
from movie_renamer import MovieRenamer
from series_renamer import SeriesRenamer

class Downloader:
	def __init__(self, filename: str, mode: str = ''):
		self.__filename = filename
		self.__mode = mode
		self.__download_dir = os.path.abspath('./downloads')
		self.lib_dir: dict = {
			'movies': '/data/Movies',
			'tvshows': '/data/Series',
			'animes': '/data/Animes',
		}
		if (not os.path.isdir(self.__download_dir)):
			os.mkdir(self.__download_dir)
		options = webdriver.FirefoxOptions()
		options = webdriver.FirefoxOptions()
		options.set_preference('browser.download.folderList', 2)
		options.set_preference('browser.download.manager.showWhenStarting', False)
		options.set_preference('browser.download.dir', self.__download_dir)
		options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
		options.add_argument('--headless')
		extension_path = os.path.abspath('./ublock_origin-1.52.2.xpi')
		self.__browser = webdriver.Firefox(options=options)
		self.__browser.set_window_position(0, 0)
		self.__browser.set_window_size(1260, 720)
		self.__browser.install_addon(extension_path)
		sleep(5)

	class __File:
		def __init__(self, filename, size, unit='Go'):
			self.filename = filename
			self.size = size
			self.unit = unit

	def __del__(self):
		self.__browser.close()

	def __check_waiting_time(self):
		try:
			time_element = self.__browser.find_element(By.CLASS_NAME, 'ct_warn')
			time = time_element.get_attribute('innerText')
			time = time.split('\n')[2]
			time = time.replace('Vous devez attendre encore ', '')
			time = time.replace(' minutes.', '')
			time = int(time)
			return (time * 60)
		except:
			return (0)

	def __close_cookie_box(self):
		try:
			self.__browser.find_element(By.CLASS_NAME, 'cookie_box_close').click()
		except:
			pass

	def __get_file_info(self):
		filename = self.__browser.find_element(By.XPATH, '/html/body/form/table/tbody/tr[1]/td[3]')
		filename = filename.get_attribute('innerText')
		size_info = self.__browser.find_element(By.XPATH, '/html/body/form/table/tbody/tr[3]/td[2]')
		size_info = size_info.get_attribute('innerText')
		size_info = size_info.split(' ')
		size_info[0] = float(size_info[0])
		return (self.__File(filename, size_info[0], size_info[1]))
	
	def __show_progress_bar(self, file, link):
		response = requests.get(link, stream=True)
		with tqdm(total=file.size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
			with open(os.path.join(self.__download_dir, file.filename), 'wb') as file:
				for chunk in response.iter_content(1024):
					if (not chunk):
						break
					file.write(chunk)
					pbar.update(len(chunk))

	def __download_link(self, link: str):
		self.__browser.get(link)
		print(f'Got link: {link}')
		sleep(2)
		self.__close_cookie_box()
		self.__browser.find_element(By.XPATH, '/html/body/div[5]/div[1]/button').click()
		file = self.__get_file_info()
		print(f"file: {file.filename}\nsize: {file.size} {file.unit}")
		if (file.unit == 'Go'):
			file.size *= 1073741824
		elif (file.unit == 'Mo'):
			file.size *= 1048576
		time = self.__check_waiting_time()
		if (time):
			current_time = datetime.datetime.now()
			time_duration = datetime.timedelta(minutes=time / 60)
			finish_time = current_time + time_duration
			print(f'waiting for {time / 60} minutes. Download will start at {finish_time}')
			wait_btn = self.__browser.find_element(By.ID, 'dlw')
			self.__browser.execute_script('arguments[0].scrollIntoView();', wait_btn)
			sleep(time)
		access_button = self.__browser.find_element(By.ID, 'dlb')
		self.__browser.execute_script('arguments[0].scrollIntoView();', access_button)
		access_button.click()
		sleep(2)
		print("Starting download")
		link = self.__browser.find_element(By.CSS_SELECTOR, '.ok').get_attribute('href')
		self.__show_progress_bar(file, link)
		renamer = None
		if self.__mode == 'movies':
			renamer = MovieRenamer()
		elif self.__mode == 'series':
			renamer = SeriesRenamer()
		if renamer:
			renamer.rename(file.filename)

	def download_files(self):
		with open(self.__filename, 'r') as file:
			while (line := file.readline()):
				line = line.strip()
				if line and not line.startswith('//'):
					self.__download_link(line)

def main():
	parser = argparse.ArgumentParser(description='Program that downloads a list of links')
	parser.add_argument('-m', '--movies', action='store_true', help='set renamer to movie mode')
	parser.add_argument('-s', '--tvshows', action='store_true', help='set renamer to tvshow mode')
	parser.add_argument('-a', '--animes', action='store_true', help='set renamer to animes mode')
	args = parser.parse_args()
	modes = vars(args)
	mode: str = ''
	for k, v in modes.items():
		if v:
			mode = k
	downloader = Downloader('./links.txt', mode=mode)
	downloader.download_files()

if (__name__ == '__main__'):
	main()
