from .base_scraper import BaseScraper
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class KiaScraper(BaseScraper):
    def __init__(self):
        url = "https://www.kia.com/tr/satis-merkezi/fiyat-listesi.html"
        super().__init__(url)

    def scrape(self) -> pd.DataFrame:
        driver = None
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument("start-maximized")
            options.add_argument("--disable-extensions")

            print("  - ChromeDriver başlatılıyor...")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_page_load_timeout(45)

            print(f"  - Sayfa isteniyor: {self.url}")
            driver.get(self.url)
            print("  - Fiyat kutularının yüklenmesi bekleniyor...")
            wait = WebDriverWait(driver, 30)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.model-price-list-box.new-type')))

            print("  - Fiyat kutuları bulundu, sayfa kaynağı okunuyor...")
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            data = []
            model_boxes = soup.find_all('div', class_='model-price-list-box new-type')

            if not model_boxes:
                print("UYARI: Kia sayfasında model kutuları bulunamadı.")
                return pd.DataFrame()

            for box in model_boxes:
                model_name = box.find('h3', class_='title').text.strip()
                for item in box.find_all('li'):
                    version = item.find('p').text.strip()
                    price = item.find('span', class_='price').text.strip()
                    data.append([model_name, version, price])

            df = pd.DataFrame(data, columns=['Model', 'Donanım', 'Fiyat'])
            df['Marka'] = 'Kia'
            print("✅ Kia verileri başarıyla çekildi.")
            return df

        except Exception as e:
            print(f"❌ HATA: Kia scraper (Selenium) çalışırken bir hata oluştu: {e}")
            return pd.DataFrame()
        finally:
            if driver:
                print("  - Kia için tarayıcı kapatılıyor.")
                driver.quit()