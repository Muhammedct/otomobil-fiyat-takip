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
            print("  - Fiyat tablosunun yüklenmesi bekleniyor...")
            wait = WebDriverWait(driver, 30)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.container table.table')))

            print("  - Tablo bulundu, sayfa kaynağı okunuyor...")
            page_source = driver.page_source
            tables = pd.read_html(page_source, flavor='lxml')

            if not tables:
                print("UYARI: Hyundai sayfasında tablo bulunamadı.")
                return pd.DataFrame()

            df = tables[0]
            df.columns = ['Model', 'Yakıt/Donanım', 'Fiyat']
            df['Marka'] = 'Hyundai'
            print("✅ Hyundai verileri başarıyla çekildi.")
            return df

        except Exception as e:
            print(f"❌ HATA: Hyundai scraper (Selenium) çalışırken bir hata oluştu: {e}")
            return pd.DataFrame()
        finally:
            if driver:
                print("  - Hyundai için tarayıcı kapatılıyor.")
                driver.quit()