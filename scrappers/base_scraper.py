import requests
from bs4 import BeautifulSoup
import pandas as pd

class BaseScraper:
    def __init__(self, url):
        self.url = url
        self.soup = self._get_soup()
        if self.soup is None:
            raise Exception(f"URL'ye erişilemedi: {self.url}")

    def _get_soup(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"URL'ye erişilirken hata oluştu: {e}")
            return None

    def scrape(self):
        raise NotImplementedError("Bu metod alt sınıflar tarafından uygulanmalıdır.")

    def get_dataframe(self):
        raise NotImplementedError("Bu metod alt sınıflar tarafından uygulanmalıdır.")