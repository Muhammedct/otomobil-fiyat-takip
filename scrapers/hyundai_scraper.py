from .base_scraper import BaseScraper
import pandas as pd
import requests

class HyundaiScraper(BaseScraper):
    def __init__(self):
        api_url = "https://www.hyundai.com/content/dam/hyundai/tr/tr/json/satin-al/fiyat-listesi-binek.json"
        super().__init__(api_url)

    def scrape(self) -> pd.DataFrame:
        print("Hyundai verileri DOĞRUDAN API'den çekiliyor...")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=20)
            response.raise_for_status()

            json_data = response.json()

            price_data = []
            for model_category in json_data.get('data', []):
                for model in model_category.get('models', []):
                    model_name = model.get('modelName')
                    for spec in model.get('specs', []):
                        donanim = spec.get('specName')
                        fiyat = spec.get('price')
                        if model_name and donanim and fiyat:
                            price_data.append([model_name, donanim, fiyat])

            if not price_data:
                print("UYARI: Hyundai API'sinden veri alınamadı veya format değişmiş.")
                return pd.DataFrame()

            df = pd.DataFrame(price_data, columns=['Model', 'Donanım', 'Fiyat'])
            df['Marka'] = 'Hyundai'
            print("✅ Hyundai verileri API'den başarıyla çekildi.")
            return df

        except Exception as e:
            print(f"❌ HATA: Hyundai API scraper çalışırken bir hata oluştu: {e}")
            return pd.DataFrame()