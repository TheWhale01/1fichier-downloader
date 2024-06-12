import os
from selenium import webdriver

class Downloader:
    def __init__(self, links: list[str]):
        self.links: list[str] = links
        self.browser = None
        self.init_browser()
    
    def __del__(self):
        self.close_browser()

    def init_browser(self):
        self.browser = webdriver.Firefox()

    def close_browser(self):
        self.browser.close()