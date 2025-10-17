from .base_scraper import BaseScraper
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class HyundaiScraper(BaseScraper):
    def __init__(self):
        url = "https://www.hyundai.com/tr/tr/satin-al/fiyat-listesi"
        super().__init__(url)

    def scrape(self) -> pd.DataFrame:
        print("Hyundai verileri Selenium ile çekiliyor...")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            driver.get(self.url)

            wait = WebDriverWait(driver, 30)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))

            page_source = driver.page_source
            tables = pd.read_html(page_source, flavor='lxml')

            if not tables:
                print("UYARI: Hyundai sayfasında tablo bulunamadı.")
                return pd.DataFrame()

            df = tables[0]
            df.columns = ['Model', 'Yakıt/Donanım', 'Fiyat']
            df['Marka'] = 'Hyundai'
            print("Hyundai verileri başarıyla çekildi.")
            return df

        except Exception as e:
            print(f"HATA: Hyundai scraper (Selenium) çalışırken bir hata oluştu: {e}")
            return pd.DataFrame()
        finally:
            if 'driver' in locals():
                driver.quit()