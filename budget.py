from config import DB_CONFIG
import psycopg2

def set_budget(user_id, category, amount):
    """تنظیم بودجه برای دسته‌بندی خاص در PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO budgets (user_id, category, amount)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, category)
            DO UPDATE SET amount = EXCLUDED.amount;
        """, (user_id, category, amount))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"[خطا در set_budget]: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return False

def get_budget(user_id, category):
    """دریافت بودجه کاربر از PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            SELECT amount FROM budgets
            WHERE user_id = %s AND category = %s;
        """, (user_id, category))
        result = cur.fetchone()
        return result[0] if result else 0
    except psycopg2.Error as e:
        print(f"[خطا در get_budget]: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return 0
