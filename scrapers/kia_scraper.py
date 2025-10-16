from .base_scraper import BaseScraper
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class KiaScraper(BaseScraper):
    def __init__(self):
        url = "https://www.kia.com/tr/satis-merkezi/fiyat-listesi.html"
        super().__init__(url)

    def scrape(self):
        if self.driver:
            try:
                self.driver.get(self.url)

                table_xpath = '//div[@class="price-list"]'
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, table_xpath))
                )

                soup = BeautifulSoup(self.driver.page_source, 'html.parser')

                price_list_container = soup.find('div', class_='price-list')
                if not price_list_container:
                    print("Kia: Fiyat listesi konteyneri bulunamadı.")
                    return

                price_tables = price_list_container.find_all('table', class_='price-list__table')

                for table in price_tables:
                    rows = table.find('tbody').find_all('tr')
                    for row in rows:
                        cols = row.find_all('td')
                        if cols and len(cols) >= 3:
                            model = cols[0].text.strip()
                            fiyat = cols[-1].text.strip().replace('TL', '').replace('.', '').strip()

                            if model and fiyat:
                                self.data.append({
                                    "Marka": "Kia",
                                    "Model": model,
                                    "Fiyat": fiyat,
                                    "Tarih": pd.Timestamp.now().strftime('%Y-%m-%d')
                                })

            except Exception as e:
                print(f"Kia Scraper Hata: {e}")
            finally:
                self.driver.quit()