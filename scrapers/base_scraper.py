import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class BaseScraper:
    def __init__(self, url):
        self.url = url
        self.driver = self._initialize_driver()
        self.data = []

    def _initialize_driver(self):
        """GitHub Actions için özel Chrome/WebDriver başlatma."""
        chrome_options = Options()
        # Headless modu: Tarayıcıyı görsel arayüz olmadan çalıştır
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")


        service = Service() # Bu varsayılan yolu kullanır

        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(30)
            return driver
        except Exception as e:
            print(f"WebDriver başlatılamadı: {e}")
            return None

    def _get_soup(self):
        """Sayfanın tam yüklendiğinden emin olup HTML'i döndürür."""
        if self.driver:
            try:
                self.driver.get(self.url)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                return BeautifulSoup(self.driver.page_source, 'html.parser')
            except Exception as e:
                print(f"URL yüklenirken hata oluştu: {e}")
                return None
        return None

    def scrape(self):
        raise NotImplementedError("Bu metod alt sınıflar tarafından uygulanmalıdır.")

    def get_dataframe(self):
        return pd.DataFrame(self.data)

    def __del__(self):
        """Scraper nesnesi silinirken tarayıcıyı kapat."""
        if self.driver:
            self.driver.quit()