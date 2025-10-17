from .base_scraper import BaseScraper
import pandas as pd
import requests # requests kütüphanesini import ediyoruz

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
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=20)
            response.raise_for_status()
            tables = pd.read_html(response.content, flavor='lxml')

            if not tables:
                print("UYARI: Hyundai sayfasında hiçbir tablo bulunamadı. Site yapısı değişmiş olabilir.")
                return pd.DataFrame()

            df = tables[0]
            df.columns = ['Model', 'Yakıt/Donanım', 'Fiyat']
            df['Marka'] = 'Hyundai'
            print("Hyundai verileri başarıyla çekildi.")
            return df

        except requests.exceptions.RequestException as e:
            print(f"HATA: Hyundai sayfasına erişirken bir ağ hatası oluştu: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"HATA: Hyundai scraper çalışırken bir hata oluştu: {e}")
            return pd.DataFrame()