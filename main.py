from selenium import webdriver
import shutil
from selenium.webdriver.common.by import By
from time import sleep
import os
import sys
import datetime
import requests
from tqdm import tqdm
import argparse
from movie_renamer import MovieRenamer
from series_renamer import SeriesRenamer

class Downloader:
	def __init__(self, filename: str, mode: str = '', output_path: str = ''):
		self.__filename = filename
		self.__mode = mode
		self.__output_path: str = output_path
		self.__download_dir = os.path.abspath('./downloads')
		self.__screenshot_dir = os.path.abspath('./screenshots')
		self.lib_dir: dict = {
			'movies': '/data/Movies',
			'tvshows': '/data/Series',
			'animes': '/data/Animes',
		}
		self.__init_browser()

	def __init_browser(self):
		if (not os.path.isdir(self.__download_dir)):
			os.mkdir(self.__download_dir)
		options = webdriver.FirefoxOptions()
		options.add_argument('--headless')
		extension_path = os.path.abspath('./ublock_origin-1.52.2.xpi')
		self.__browser = webdriver.Firefox(options=options)
		self.__browser.set_window_position(0, 0)
		self.__browser.maximize_window()
		self.__browser.install_addon(extension_path)

	class __File:
		def __init__(self, filename, size, unit='Go'):
			self.filename = filename
			self.size = size
			self.unit = unit

	def __del__(self):
		self.__browser.close()

	def __check_waiting_time(self):
		try:
			time_element = self.__browser.find_element(By.CSS_SELECTOR, 'div.ct_warn:nth-child(3)')
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
			self.__browser.find_element(By.CSS_SELECTOR, 'button.ui-button').click()
		except:
			return

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
		self.__browser.close()
		with tqdm(total=file.size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
			with open(os.path.join(self.__download_dir, file.filename), 'wb') as file:
				for chunk in response.iter_content(1024):
					if (not chunk):
						break
					file.write(chunk)
					pbar.update(len(chunk))
		self.__init_browser()

	def __download_link(self, link: str):
		self.__browser.get(link)
		print(f'Got link: {link}')
		sleep(2)
		self.__close_cookie_box()
		file = self.__get_file_info()
		print(f"file: {file.filename}\nsize: {file.size} {file.unit}")
		if (file.unit == 'Go'):
			file.size *= 1073741824
		elif (file.unit == 'Mo'):
			file.size *= 1048576
		time = self.__check_waiting_time()
		if (time):
			self.__browser.close()
			current_time = datetime.datetime.now()
			time_duration = datetime.timedelta(minutes=time / 60)
			finish_time = current_time + time_duration
			print(f'waiting for {time / 60} minutes. Download will start at {finish_time}')
			sleep(time)
			self.__init_browser()
			self.__browser.get(link)
			sleep(2)
			self.__close_cookie_box()
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
			renamer = SeriesRenamer(self.lib_dir[self.__mode])
		if renamer:
			renamer.rename(file.filename)
		elif self.__output_path:
			shutil.move(os.path.join(self.__download_dir, file.filename), self.__output_path)

	def download_files(self):
		error_nb: int = 0
		with open(self.__filename, 'r') as file:
			while (line := file.readline()):
				line = line.strip()
				if line and not line.startswith('//'):
					try:
						self.__download_link(line)
					except:
						print(f"Could not download link: {line}", file=sys.stderr)
						self.__browser.get_screenshot_as_file(f'{self.__screenshot_dir}/error_{error_nb}.png')
						error_nb += 1

def main():
	parser = argparse.ArgumentParser(description='Program that downloads a list of links')
	parser.add_argument('-m', '--movies', action='store_true', help='set renamer to movie mode')
	parser.add_argument('-s', '--tvshows', action='store_true', help='set renamer to tvshow mode')
	parser.add_argument('-a', '--animes', action='store_true', help='set renamer to animes mode')
	parser.add_argument('-p', '--path', help='path where the downloaded file should be')
	args = parser.parse_args()
	modes = vars(args)
	mode: str = ''
	for k, v in modes.items():
		if v:
			mode = k
	downloader = Downloader('./links.txt', mode=mode, output_path=modes['path'])
	downloader.download_files()

if (__name__ == '__main__'):
	main()
