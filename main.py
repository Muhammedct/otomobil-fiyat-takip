import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from datetime import datetime
from scrapers.hyundai_scraper import HyundaiScraper
from scrapers.kia_scraper import KiaScraper


GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")

def scrape_and_save():
    """Tüm scraper'ları çalıştırır ve veriyi Excel'e kaydeder."""
    scrapers = {
        "Hyundai": HyundaiScraper(),
        "Kia": KiaScraper()
    }

    excel_filename = f"otomobil_fiyatlari_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    archive_path = os.path.join("data_archive", excel_filename)

    with pd.ExcelWriter(archive_path) as writer:
        for brand, scraper in scrapers.items():
            print(f"{brand} için veriler kazınıyor...")
            try:
                scraper.scrape()
                df = scraper.get_dataframe()
                if not df.empty:
                    df.to_excel(writer, sheet_name=brand, index=False)
                    print(f"{brand} verileri başarıyla alındı.")
                else:
                    print(f"{brand} için veri bulunamadı.")
            except Exception as e:
                print(f"Hata: {brand} scraper çalışırken bir hata oluştu - {e}")

    return archive_path

def send_email(file_path):
    """Excel dosyasını e-posta ile gönderir."""
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"Güncel Otomobil Fiyatları - {datetime.now().strftime('%Y-%m-%d')}"

        body = "Merhaba,\n\nEkte güncel otomobil fiyat listesi bulunmaktadır.\n\nSevgilerle,\nFiyat Takip Botu"
        msg.attach(MIMEText(body, 'plain'))

        # Dosyayı e-postaya ekle
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(file_path)}",
            )
            msg.attach(part)

        # SMTP Sunucusuna Bağlanma ve E-posta Gönderme
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            text = msg.as_string()
            server.sendmail(GMAIL_USER, RECEIVER_EMAIL, text)

        print("E-posta başarıyla gönderildi!")

    except Exception as e:
        print(f"E-posta gönderilirken bir hata oluştu: {e}")

if __name__ == "__main__":
    if not os.path.exists('data_archive'):
        os.makedirs('data_archive')

    excel_file = scrape_and_save()
    send_email(excel_file)