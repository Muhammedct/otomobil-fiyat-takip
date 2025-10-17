# main.py

import pandas as pd
from scrapers.hyundai_scraper import HyundaiScraper
from scrapers.kia_scraper import KiaScraper
from utils.excel_handler import save_to_excel, read_from_excel, compare_dataframes
from utils.email_handler import send_email
from datetime import datetime

EXCEL_FILENAME = "otomobil_fiyatlari.xlsx"

def scrape_and_process():
    """Tüm markaların verilerini çeker ve birleştirir."""
    scrapers = {
        "Hyundai": HyundaiScraper(),
        "Kia": KiaScraper(),
    }

    all_data = []
    for brand, scraper_instance in scrapers.items():
        try:
            df = scraper_instance.scrape()
            if not df.empty:
                all_data.append(df)
        except Exception as e:
            print(f"HATA: {brand} scraper'ı çalıştırılırken bir hata oluştu: {e}")

    if not all_data:
        print("Hiçbir markadan veri çekilemedi. İşlem sonlandırılıyor.")
        return None

    return pd.concat(all_data, ignore_index=True)

if __name__ == "__main__":
    start_time = datetime.now()
    print(f"İşlem başladı: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    old_data = read_from_excel(EXCEL_FILENAME)
    new_data = scrape_and_process()

    if new_data is not None and not new_data.empty:
        has_changed, changes_summary = compare_dataframes(old_data, new_data)

        if has_changed:
            print("Fiyat listesinde değişiklik tespit edildi. Bildirim hazırlanıyor...")
            email_subject = "Otomobil Fiyatlarında Değişiklik Tespit Edildi!"
            email_body = f"Merhaba,\n\nAraç fiyat listelerinde aşağıdaki değişiklikler tespit edilmiştir:\n\n{changes_summary}"

            send_email(email_subject, email_body)
            save_to_excel(new_data, EXCEL_FILENAME)
        else:
            print("Fiyatlarda herhangi bir değişiklik bulunamadı.")
    else:
        print("Yeni veri alınamadığı için karşılaştırma yapılamadı.")

    end_time = datetime.now()
    print(f"İşlem tamamlandı: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Toplam süre: {end_time - start_time}")