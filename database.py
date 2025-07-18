# database.py
import os
import psycopg2
from urllib.parse import urlparse

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def insert_transaction(user_id: int, amount: float, t_type: str):
    """درج درآمد یا هزینه در جدول transactions"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions (user_id, amount, type) VALUES (%s, %s, %s)",
        (user_id, amount, t_type)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_monthly_totals(user_id: int):
    """برگرداندن مجموع درآمد و هزینه کاربر در ماه جاری"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT type, COALESCE(SUM(amount),0) 
        FROM transactions 
        WHERE user_id=%s 
          AND date_trunc('month', created_at)=date_trunc('month', CURRENT_DATE)
        GROUP BY type
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # تبدیل به دیکشن {'income': X, 'expense': Y}
    return { r[0]: float(r[1]) for r in rows }
