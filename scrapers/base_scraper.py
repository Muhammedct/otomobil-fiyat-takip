from abc import ABC, abstractmethod
import pandas as pd

class BaseScraper(ABC):
    """
    Tüm scraper sınıfları için bir temel (soyut) sınıf.
    Her scraper'ın bir URL'si olmalı ve 'scrape' metodunu içermelidir.
    """
    def __init__(self, url: str):
        if not url:
            raise ValueError("URL boş olamaz.")
        self.url = url

    @abstractmethod
    def scrape(self) -> pd.DataFrame:
        """
        Web sitesinden verileri çeker ve bir pandas DataFrame olarak döndürür.
        Bu metodun her alt scraper sınıfında override edilmesi zorunludur.
        """
        pass