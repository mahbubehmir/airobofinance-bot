import psycopg2
from psycopg2 import sql
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from config import DB_CONFIG

def get_monthly_transactions(user_id, month):
    """
    دریافت تراکنش‌های یک کاربر در یک ماه خاص.
    month باید به صورت 'YYYY-MM' باشد، مثلاً '2025-07'.
    خروجی: لیستی از تاپل‌ها: [(date, amount, type, category), ...]
    """
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        query = sql.SQL("""
            SELECT
                created_at::date AS date,
                amount,
                type,
                category
            FROM transactions
            WHERE user_id = %s
              AND to_char(created_at, 'YYYY-MM') = %s
            ORDER BY created_at;
        """)
        cur.execute(query, (user_id, month))
        return cur.fetchall()
    except Exception as e:
        print(f"❌ خطا در دریافت تراکنش‌ها: {e}")
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def generate_monthly_report(user_id, month):
    """
    تولید گزارش ماهانه با نمودار و جدول خلاصه.
    مقدار برگشتی: (BytesIO تصویر نمودار PNG, رشته جدول خلاصه)
    """
    # دریافت داده‌ها
    transactions = get_monthly_transactions(user_id, month)
    df = pd.DataFrame(transactions, columns=['date', 'amount', 'type', 'category'])
    
    # اگر هیچ داده‌ای نبود، خروجی مناسب بده
    if df.empty:
        # تصویر خالی با پیام
        plt.figure(figsize=(6, 4))
        plt.text(0.5, 0.5, 'هیچ تراکنشی ثبت نشده', ha='center', va='center')
        plt.axis('off')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf, "هیچ تراکنشی در این ماه ثبت نشده."

    # تبدیل ستون تاریخ
    df['date'] = pd.to_datetime(df['date'])
    
    # جدول خلاصه
    summary = (
        df.groupby(['type', 'category'])['amount']
          .sum()
          .reset_index()
    )
    
    # تولید نمودار هزینه‌ها
    expenses = df[df['type'] == 'expense']
    plt.figure(figsize=(10, 6))
    if not expenses.empty:
        expenses.groupby('category')['amount'].sum().plot.pie(
            autopct='%1.1f%%',
            startangle=90,
            shadow=True
        )
        plt.title('توزیع هزینه‌های ماهانه')
        plt.axis('equal')
    else:
        plt.text(0.5, 0.5, 'هیچ هزینه‌ای در این ماه ثبت نشده',
                 ha='center', va='center')
        plt.axis('off')
    
    # ذخیره در حافظه
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()
    img_buffer.seek(0)
    
    return img_buffer, summary.to_string(index=False)

# برای تست مستقیم این فایل:
if __name__ == '__main__':
    # مثال تست: user_id=1، ماه '2025-07'
    img, table = generate_monthly_report(user_id=1, month='2025-07')
    with open('monthly_report.png', 'wb') as f:
        f.write(img.getvalue())
    print(table)
