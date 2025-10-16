from .base_scraper import BaseScraper
import pandas as pd

class KiaScraper(BaseScraper):
    def __init__(self):
        url = "https://www.kia.com/tr/satis-merkezi/fiyat-listesi.html"
        super().__init__(url)
        self.data = []

    def scrape(self):
        if self.soup:
            table = self.soup.find('table', class_='price-list')
            if not table:
                print("Kia fiyat listesi tablosu bulunamadı.")
                return

            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                if cols:
                    self.data.append({
                        "Model": cols[0],
                        "Fiyat": cols[1],
                        "Tarih": pd.Timestamp.now().strftime('%Y-%m-%d')
                    })

    def get_dataframe(self):
        return pd.DataFrame(self.data)