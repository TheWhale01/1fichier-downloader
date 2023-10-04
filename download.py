from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os

def get_links(filename: str()) -> list(str()):
	links = []
	with open(filename, 'r') as file:
		for line in file.readlines():
			if (not line.startswith('//')):
				links.append(line.replace('\n', ''))
	return (links)

def is_part_file(directory: str()) -> bool():
	for file in os.listdir(directory):
		if (file.endswith('.part')):
			return (True)
	return (False)

def init(download_dir: str()) -> webdriver.firefox.webdriver.WebDriver:
	options = webdriver.FirefoxOptions()
	options.set_preference('browser.download.folderList', 2)
	options.set_preference('browser.download.manager.showWhenStarting', False)
	options.set_preference('browser.download.dir', download_dir)
	options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
	options.add_argument('--headless')
	extension_path = os.path.abspath('./ublock_origin-1.52.2.xpi')
	browser = webdriver.Firefox(options=options)
	browser.install_addon(extension_path)
	sleep(5)
	return (browser)

def main():
	if (not os.path.isdir('./downloads/')):
		os.makedir('./downloads/')
	download_dir = os.path.abspath('./downloads/')
	browser = init(download_dir)
	links = get_links('links.txt')
	for link in links:
		print('Link accessed.')
		browser.get(link)
		sleep(5)
		browser.find_element(By.XPATH, '/html/body/div[5]/div[1]/button').click()
		sleep(1)
		access_button = browser.find_element(By.ID, 'dlb')
		print('Waiting for access button.')
		while (True):
			try:
				access_button.click()
				break
			except:
				sleep(60)
		browser.find_element(By.XPATH, '/html/body/div[4]/div[2]/a').click()
		print('download started.')
		while (is_part_file(download_dir)):
			sleep(60)
	browser.close()

if (__name__ == '__main__'):
    main()
