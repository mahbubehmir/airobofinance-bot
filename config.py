import os
from dotenv import load_dotenv
import psycopg2
import logging

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

# اتصال به دیتابیس
def connect_db():
    return psycopg2.connect(DATABASE_URL)
