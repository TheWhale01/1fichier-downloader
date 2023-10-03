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

def downloading_file(directory: str()) -> bool():
	for file in os.listdir(directory):
		if (file.endswith('.crdownload')):
			return (True)
	return (False)

def init(download_dir: str()) -> webdriver.chrome.webdriver.ChromiumDriver:
	options = webdriver.ChromeOptions()
	options.binary_location = '/bin/'
	# options.add_argument('--headless')
	options.add_experimental_option("prefs", {
		'download.default_directory': download_dir,
	})
	extension_path = os.path.abspath('./cjpalhdlnbpafiamejdnhcphjbkeiagm.crx')
	options.add_extension(extension_path)
	browser = webdriver.Chrome(options=options)
	sleep(5)
	return (browser)

def main():
	if (not os.path.isdir('./downloads/')):
		os.mkdir('./downloads/')
	download_dir = os.path.abspath('./downloads/')
	browser = init(download_dir)
	links = get_links('links.txt')
	for link in links:
		browser.get(link)
		sleep(5)
		browser.find_element(By.XPATH, '/html/body/div[5]/div[1]/button').click()
		sleep(4)
		access_button = browser.find_element(By.ID, 'dlb')
		print("Waiting for access button to be clickable")
		while (True):
			try:
				access_button.click()
				break
			except:
				sleep(60)
		browser.find_element(By.XPATH, "/html/body/div[1]/a[2]").click()
		sleep(1)
		browser.find_element(By.XPATH, '/html/body/div[4]/div[2]/a').click()
		print('Downloading file.')
		while (downloading_file(download_dir)):
			sleep(60)

if (__name__ == '__main__'):
	main()
