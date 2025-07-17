import os
from dotenv import load_dotenv

load_dotenv()

# توکن ربات
TOKEN = os.getenv('BOT_TOKEN')

# اطلاعات اتصال به پایگاه داده
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}
