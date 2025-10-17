from .base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup
import pandas as pd

class KiaScraper(BaseScraper):
    """
    Kia Türkiye fiyat listesi sayfasından veri çekmek için scraper.
    """
    def __init__(self):
        url = "https://www.kia.com/tr/satis-merkezi/fiyat-listesi.html"
        super().__init__(url)

    def scrape(self) -> pd.DataFrame:
        print("Kia verileri çekiliyor...")
        try:
            response = requests.get(self.url, timeout=15)
            response.raise_for_status() # HTTP hata kontrolü
            soup = BeautifulSoup(response.content, 'html.parser')

            data = []
            model_boxes = soup.find_all('div', class_='model-price-list-box')

            for box in model_boxes:
                model_name_tag = box.find('h3', class_='title')
                model_name = model_name_tag.text.strip() if model_name_tag else "Bilinmeyen Model"

                price_items = box.find_all('li')
                for item in price_items:
                    version_tag = item.find('p')
                    price_tag = item.find('span', class_='price')

                    if version_tag and price_tag:
                        version = version_tag.text.strip()
                        price = price_tag.text.strip()
                        data.append([model_name, version, price])

            if not data:
                print("UYARI: Kia sayfasında veri bulunamadı. Site yapısı değişmiş olabilir.")
                return pd.DataFrame()

            df = pd.DataFrame(data, columns=['Model', 'Donanım', 'Fiyat'])
            df['Marka'] = 'Kia'
            print("Kia verileri başarıyla çekildi.")
            return df

        except requests.exceptions.RequestException as e:
            print(f"HATA: Kia sayfasına erişirken bir ağ hatası oluştu: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"HATA: Kia scraper çalışırken bir hata oluştu: {e}")
            return pd.DataFrame()