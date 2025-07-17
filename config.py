import os
from dotenv import load_dotenv
import psycopg2
import urllib.parse as urlparse

load_dotenv()

# بارگذاری آدرس کامل دیتابیس از فایل env
DATABASE_URL = os.getenv("DATABASE_URL")

# تجزیه URL برای گرفتن اجزای اتصال
url = urlparse.urlparse(DATABASE_URL)

DB_CONFIG = {
    'dbname': url.path[1:],
    'user': url.username,
    'password': url.password,
    'host': url.hostname,
    'port': url.port
}

# توکن ربات
BOT_TOKEN = os.getenv("BOT_TOKEN")


if __name__ == "__main__":
    print("✅ فایل config.py با موفقیت اجرا شد.")
    print("توکن:", BOT_TOKEN)
    print("تنظیمات دیتابیس:", DB_CONFIG)
