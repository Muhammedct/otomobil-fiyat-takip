from .base_scraper import BaseScraper
import pandas as pd

class HyundaiScraper(BaseScraper):
    """
    Hyundai Türkiye fiyat listesi sayfasından veri çekmek için scraper.
    """
    def __init__(self):
        url = "https://www.hyundai.com/tr/tr/satin-al/fiyat-listesi"
        super().__init__(url)

    def scrape(self) -> pd.DataFrame:
        print("Hyundai verileri çekiliyor...")
        try:
            tables = pd.read_html(self.url, flavor='lxml')

            if not tables:
                print("Hyundai sayfasında hiçbir tablo bulunamadı.")
                return pd.DataFrame()

            df = tables[0]
            df.columns = ['Model', 'Yakıt/Donanım', 'Fiyat']
            df['Marka'] = 'Hyundai'
            print("Hyundai verileri başarıyla çekildi.")
            return df

        except Exception as e:
            print(f"HATA: Hyundai scraper çalışırken bir hata oluştu: {e}")
            return pd.DataFrame()