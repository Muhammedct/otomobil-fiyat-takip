import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os

class BaseScraper:
    def __init__(self, url):
        self.url = url
        self.driver = self._initialize_driver()
        self.data = []

    def _initialize_driver(self):
        """GitHub Actions için özel Chrome/WebDriver başlatma."""
        chrome_options = Options()

        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        service = Service(service_log_path=os.devnull)

        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(45)
            return driver
        except Exception as e:
            print(f"WebDriver başlatılamadı. Chrome kurulu ve PATH'e ekli mi? Hata: {e}")
            return None

    def scrape(self):
        """Bu metodun alt sınıflarda uygulanması zorunludur."""
        raise NotImplementedError("Bu metod alt sınıflar tarafından uygulanmalıdır.")

    def get_dataframe(self):
        return pd.DataFrame(self.data)

    def __del__(self):
        """Scraper nesnesi silinirken tarayıcıyı kapat."""
        if self.driver:
            self.driver.quit()