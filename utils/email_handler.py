import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

def send_email(subject: str, body: str):
    """Değişiklikleri içeren bir e-posta gönderir."""
    if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER]):
        print("HATA: Gerekli çevre değişkenleri (EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER) ayarlanmamış.")
        print("Lütfen GitHub repository Secrets ayarlarınızı kontrol edin.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            print("Değişiklik bildirimi e-postası başarıyla gönderildi.")

    except smtplib.SMTPAuthenticationError:
        print("HATA: E-posta gönderilemedi. SMTP kimlik doğrulaması başarısız.")
        print("Lütfen GitHub Secrets'daki EMAIL_SENDER ve EMAIL_PASSWORD bilgilerini kontrol edin.")
    except Exception as e:
        print(f"HATA: E-posta gönderirken bir sorun oluştu: {e}")