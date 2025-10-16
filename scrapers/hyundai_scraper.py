from .base_scraper import BaseScraper
import pandas as pd

class HyundaiScraper(BaseScraper):
    def __init__(self):
        url = "https://www.hyundai.com/tr/tr/arac-satis/arac-fiyat-listesi"
        super().__init__(url)
        self.data = []

    def scrape(self):
        if self.soup:
            price_list = self.soup.find('div', class_='price-list-table')
            if not price_list:
                print("Hyundai fiyat listesi tablosu bulunamadı.")
                return

            rows = price_list.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                cols = [ele.text.strip() for ele in cols]
                if cols and len(cols) > 2:
                    self.data.append({
                        "Model": cols[0],
                        "Fiyat": cols[1],
                        "Tarih": pd.Timestamp.now().strftime('%Y-%m-%d')
                    })

    def get_dataframe(self):
        return pd.DataFrame(self.data)