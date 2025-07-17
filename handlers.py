from telegram import ReplyKeyboardMarkup
from datetime import datetime

# لیست موقت برای ذخیره تراکنش‌ها
transactions = []
budgets = {}

def start(update, context):
    user = update.message.from_user
    update.message.reply_text(
        f"سلام {user.first_name}! به ربات مدیریت مالی خوش آمدید.\n"
        "لطفاً از منوی زیر انتخاب کنید:",
        reply_markup=main_menu()
    )

def record_income(update, context):
    update.message.reply_text("لطفاً مبلغ درآمد را وارد کنید:")

def record_expense(update, context):
    update.message.reply_text("لطفاً مبلغ هزینه را وارد کنید:")

def show_report(update, context):
    user_id = update.message.from_user.id
    total_income = sum(t[1] for t in transactions if t[0] == user_id and t[3] == 'income')
    total_expense = sum(t[1] for t in transactions if t[0] == user_id and t[3] == 'expense')
    
    report = (
        f"📊 گزارش مالی:\n"
        f"➖ مجموع درآمدها: {total_income:,} تومان\n"
        f"➖ مجموع هزینه‌ها: {total_expense:,} تومان\n"
        f"➖ مانده حساب: {total_income - total_expense:,} تومان"
    )
    
    if user_id in budgets:
        report += f"\n\n💰 بودجه ماهانه: {budgets[user_id]:,} تومان"
        remaining = budgets[user_id] - total_expense
        report += f"\n➖ باقی‌مانده بودجه: {remaining:,} تومان"
    
    update.message.reply_text(report)

def set_budget(update, context):
    update.message.reply_text("لطفاً مبلغ بودجه ماهانه را وارد کنید:")

def main_menu():
    return ReplyKeyboardMarkup(
        [['📊 گزارش', '➕ درآمد'], ['➖ هزینه', '💰 تنظیم بودجه']],
        resize_keyboard=True
    )