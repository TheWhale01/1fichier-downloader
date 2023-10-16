from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
import sys
import datetime
from tqdm import tqdm

class Downloader:
	def __init__(self, filename: str()):
		self.__filename = filename
		self.__chunk_size = 1024
		self.__download_dir = os.path.abspath('./downloads')
		if (not os.path.isdir(self.__download_dir)):
			os.mkdir(self.__download_dir)
		options = webdriver.FirefoxOptions()
		options = webdriver.FirefoxOptions()
		options.set_preference('browser.download.folderList', 2)
		options.set_preference('browser.download.manager.showWhenStarting', False)
		options.set_preference('browser.download.dir', self.__download_dir)
		options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
		# options.add_argument('--headless')
		extension_path = os.path.abspath('./ublock_origin-1.52.2.xpi')
		self.__browser = webdriver.Firefox(options=options)
		self.__browser.set_window_position(0, 0)
		self.__browser.set_window_size(1260, 720)
		self.__browser.install_addon(extension_path)
		sleep(5)

	def __del__(self):
		self.__browser.close()

	def __check_part_file(self):
		os.chdir(self.__download_dir)
		return (not len(glob.glob('*.part')))

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
		return (0)

	def __close_cookie_box(self):
		try:
			self.__browser.find_element(By.CLASS_NAME, 'cookie_box_close').click()
		except:
			pass

	def __get_file_info(self):
		filename = self.__browser.find_element(By.XPATH, '/html/body/form/table/tbody/tr[1]/td[3]')
		filename = filename.get_attribute('innerText')
		size = self.__browser.find_element(By.XPATH, '/html/body/form/table/tbody/tr[3]/td[2]')
		size = size.get_attribute('innerText')
		return (filename, size)
	
	def __show_progress_bar(self, size):
		os.chdir(self.__download_dir)
		part_file = glob.glob(('*.part'))
		with tqdm(total=size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
			while True:
				current_size = os.path.getsize(os.path.join(self.__download_dir, part_file))
				pbar.update(current_size - pbar.n)
				if (current_size == size):
					break
				sleep(1)

	def __download_link(self, link: str()):
		self.__browser.get(link)
		print(f'Got link: {link}')
		sleep(2)
		self.__close_cookie_box()

		# Close premium box
		self.__browser.find_element(By.XPATH, '/html/body/div[5]/div[1]/button').click()

		filename, size = self.__get_file_info()
		print(filename, size)
		print(f"file: {filename}\nsize: {size}")
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
		self.__browser.find_element(By.XPATH, '/html/body/div[4]/div[2]/a').click()
		self.__show_progress_bar(size)

	def download_files(self):
		with open(self.__filename, 'r') as file:
			while (line := file.readline()):
				line = line.strip()
				if line and not line.startswith('//'):
					self.__download_link(line)

# def get_links(filename: str()) -> list(str()):
#	  links = []
#	  with open(filename, 'r') as file:
#		  for line in file.readlines():
#			  line = line.replace('\n', '')
#			  if (not line.startswith('//') and line):
#				  links.append(line)
#	  return (links)
# 
# def is_part_file(directory: str()) -> bool():
#	  for file in os.listdir(directory):
#		  if (file.endswith('.part')):
#			  return (True)
#	  return (False)
# 
# def check_waiting_time(browser):
#	  try:
#		  time_element = browser.find_element(By.CLASS_NAME, 'ct_warn')
#		  time = time_element.get_attribute('innerText')
#		  time = time.split('\n')[2]
#		  time = time.replace('Vous devez attendre encore ', '')
#		  time = time.replace(' minutes.', '')
#		  time = int(time)
#		  return (time * 60)
#	  except:
#		  return (0)
#	  return (0)
# 

# def main():
#	  if (not os.path.isdir('./downloads/')):
#		  os.mkdir('./downloads/')
#	  download_dir = os.path.abspath('./downloads/')
#	  browser = init(download_dir)
#	  links = get_links('links.txt')
#	  for link in links:
#		  print('Link accessed.')
#		  browser.get(link)
#		  sleep(5)
#		  try:
#			  browser.find_element(By.CLASS_NAME, 'cookie_box_close').click()
#		  except:
#			  pass
#		  browser.find_element(By.XPATH, '/html/body/div[5]/div[1]/button').click()
#		  time = check_waiting_time(browser)
#		  if (time):
#			  current_time = datetime.datetime.now()
#			  time_duration = datetime.timedelta(minutes=time / 60)
#			  finish_time = current_time + time_duration
#			  print(f'waiting for {time / 60} minutes. Download will start at {finish_time}')
#			  wait_btn = browser.find_element(By.ID, 'dlw')
#			  browser.execute_script('arguments[0].scrollIntoView();', wait_btn)
#			  sleep(time)
#		  print('wait finished.')
#		  access_button = browser.find_element(By.ID, 'dlb')
#		  browser.execute_script('arguments[0].scrollIntoView();', access_button)
#		  if (not access_button.is_displayed()):
#			  sleep(60)
#		  access_button.click()
#		  sleep(2)
#		  browser.find_element(By.XPATH, '/html/body/div[4]/div[2]/a').click()
#		  sleep(5)
#		  print('download started.')
#		  while (is_part_file(download_dir)):
#			  sleep(60)
#	  browser.close()

def main():
	downloader = Downloader('./links.txt')
	downloader.download_files()

if (__name__ == '__main__'):
	main()
