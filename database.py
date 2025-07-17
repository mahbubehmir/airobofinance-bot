import psycopg2
from psycopg2 import sql
from config import DB_CONFIG
import logging

# تنظیمات لاگ‌گیری
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """ایجاد جداول مورد نیاز در دیتابیس"""
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        logger.info("اتصال به دیتابیس برقرار شد. در حال ایجاد جداول...")
        
        # ایجاد جدول کاربران
        cur.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE NOT NULL,
                username VARCHAR(100),
                full_name VARCHAR(200),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # ایجاد جدول تراکنش‌ها
        cur.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
                type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
                category VARCHAR(50) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # ایجاد جدول بودجه‌ها
        cur.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS budgets (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                category VARCHAR(50) NOT NULL,
                amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (user_id, category)
            );
        """))
        
        # ایندکس برای بهبود عملکرد
        cur.execute(sql.SQL("""
            CREATE INDEX IF NOT EXISTS idx_transactions_user_date 
            ON transactions(user_id, created_at);
        """))
        
        conn.commit()
        logger.info("✅ جداول با موفقیت ایجاد شدند.")
        
    except psycopg2.OperationalError as e:
        logger.error(f"❌ خطای اتصال به دیتابیس: {e}")
    except psycopg2.Error as e:
        logger.error(f"❌ خطا در اجرای کوئری: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# ✅ اجرای تابع
if __name__ == '__main__':
    create_tables()
