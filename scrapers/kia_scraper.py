from .base_scraper import BaseScraper
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup

class KiaScraper(BaseScraper):
    def __init__(self):
        url = "https://www.kia.com/tr/satis-merkezi/fiyat-listesi.html"
        super().__init__(url)

    def scrape(self) -> pd.DataFrame:
        print("Kia verileri DOĞRUDAN sayfa kaynağından (JS objesi) çekiliyor...")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=20)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            script_tag = soup.find('script', string=lambda t: 'gtmModelPriceData' in str(t))

            if not script_tag:
                print("UYARI: Kia sayfasında fiyat verisini içeren script etiketi bulunamadı.")
                return pd.DataFrame()

            script_content = script_tag.string
            json_str = script_content.split('gtmModelPriceData: ')[1].split(';\n')[0]
            json_data = json.loads(json_str)

            price_data = []
            for model_data in json_data:
                model_name = model_data.get('modelName')
                for trim in model_data.get('trim', []):
                    donanim = trim.get('name')
                    fiyat = trim.get('price')
                    if model_name and donanim and fiyat:
                        price_data.append([model_name, donanim, str(fiyat)])

            if not price_data:
                print("UYARI: Kia verisi okunamadı veya format değişmiş.")
                return pd.DataFrame()

            df = pd.DataFrame(price_data, columns=['Model', 'Donanım', 'Fiyat'])
            df['Marka'] = 'Kia'
            print("✅ Kia verileri başarıyla çekildi.")
            return df

        except Exception as e:
            print(f"❌ HATA: Kia scraper çalışırken bir hata oluştu: {e}")
            return pd.DataFrame()