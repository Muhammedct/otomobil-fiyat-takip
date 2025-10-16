import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class BaseScraper:

    def _initialize_driver(self):
        """GitHub Actions için özel Chrome/WebDriver başlatma."""
        chrome_options = Options()

        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--dns-prefetch-disable")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


        service = Service(service_log_path=os.devnull)

        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(60)
            return driver
        except Exception as e:
            print(f"WebDriver başlatılamadı. Chrome kurulu ve PATH'e ekli mi? Hata: {e}")
            return None