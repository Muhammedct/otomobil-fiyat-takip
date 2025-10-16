from .base_scraper import BaseScraper
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HyundaiScraper(BaseScraper):
    def __init__(self):
        url = "https://www.hyundai.com/tr/tr/arac-satis/arac-fiyat-listesi"
        BaseScraper.__init__(self, url)

    def scrape(self):
        if self.driver:
            try:
                self.driver.get(self.url)

                table_xpath = '//table[@class="price-table"]'
                WebDriverWait(self.driver, 25).until( # Saniye artırıldı
                    EC.presence_of_element_located((By.XPATH, table_xpath))
                )

                soup = BeautifulSoup(self.driver.page_source, 'html.parser')

                price_list_table = soup.find('table', class_='price-table')
                if not price_list_table:
                    print("Hyundai: Fiyat tablosu (price-table) bulunamadı.")
                    return

                rows = price_list_table.find('tbody').find_all('tr')

                for row in rows:
                    cols = row.find_all('td')
                    if cols and len(cols) >= 3:
                        model = cols[0].text.strip()
                        fiyat = cols[-1].text.strip().replace('TL', '').replace('.', '').strip()

                        if model and fiyat:
                            self.data.append({
                                "Marka": "Hyundai",
                                "Model": model,
                                "Fiyat": fiyat,
                                "Tarih": pd.Timestamp.now().strftime('%Y-%m-%d')
                            })

            except Exception as e:
                print(f"Hyundai Scraper Hata: {e}")