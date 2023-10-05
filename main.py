from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
import sys
import datetime

def get_links(filename: str()) -> list(str()):
    links = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            line = line.replace('\n', '')
            if (not line.startswith('//') and line):
                links.append(line)
    return (links)

def is_part_file(directory: str()) -> bool():
    for file in os.listdir(directory):
        if (file.endswith('.part')):
            return (True)
    return (False)

def check_waiting_time(browser):
    try:
        time_element = browser.find_element(By.CLASS_NAME, 'ct_warn')
        time = time_element.get_attribute('innerText')
        time = time.split('\n')[2]
        time = time.replace('Vous devez attendre encore ', '')
        time = time.replace(' minutes.', '')
        time = int(time)
        return (time * 60)
    except:
        return (0)
    return (0)

def init(download_dir: str()) -> webdriver.firefox.webdriver.WebDriver:
    options = webdriver.FirefoxOptions()
    options.set_preference('browser.download.folderList', 2)
    options.set_preference('browser.download.manager.showWhenStarting', False)
    options.set_preference('browser.download.dir', download_dir)
    options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
    options.add_argument('--headless')
    extension_path = os.path.abspath('./ublock_origin-1.52.2.xpi')
    browser = webdriver.Firefox(options=options)
    browser.set_window_position(0, 0)
    browser.set_window_size(1260, 720)
    browser.install_addon(extension_path)
    sleep(5)
    return (browser)

def main():
    if (not os.path.isdir('./downloads/')):
        os.mkdir('./downloads/')
    download_dir = os.path.abspath('./downloads/')
    browser = init(download_dir)
    links = get_links('links.txt')
    for link in links:
        print('Link accessed.')
        browser.get(link)
        sleep(5)
        try:
            browser.find_element(By.CLASS_NAME, 'cookie_box_close').click()
        except:
            pass
        browser.find_element(By.XPATH, '/html/body/div[5]/div[1]/button').click()
        time = check_waiting_time(browser)
        if (time):
            current_time = datetime.datetime.now()
            time_duration = datetime.timedelta(minutes=time / 60)
            finish_time = current_time + time_duration
            print(f'waiting for {time / 60} minutes. Download will start at {finish_time}')
            wait_btn = browser.find_element(By.ID, 'dlw')
            browser.execute_script('arguments[0].scrollIntoView();', wait_btn)
            sleep(time)
        print('wait finished.')
        access_button = browser.find_element(By.ID, 'dlb')
        browser.execute_script('arguments[0].scrollIntoView();', access_button)
        if (not access_button.is_displayed()):
            sleep(60)
        access_button.click()
        sleep(2)
        browser.find_element(By.XPATH, '/html/body/div[4]/div[2]/a').click()
        sleep(5)
        print('download started.')
        while (is_part_file(download_dir)):
            sleep(60)
    browser.close()

if (__name__ == '__main__'):
    main()
