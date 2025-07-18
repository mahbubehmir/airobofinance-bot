from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, CommandHandler, filters
from datetime import datetime
AMOUNT_INCOME, AMOUNT_EXPENSE, AMOUNT_BUDGET = range(3)

# Conversation states
AMOUNT = 1

# In-memory storage
transactions = []  # list of tuples (user_id, amount, type, timestamp)
budgets = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f"سلام {user.first_name}! به ربات مدیریت مالی خوش آمدید.",
        reply_markup=main_menu()
    )
    return ConversationHandler.END

# Entry points for income and expense
async def record_income_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفاً مبلغ درآمد را به عدد وارد کنید:")
    context.user_data['type'] = 'income'
    return AMOUNT

async def record_expense_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفاً مبلغ هزینه را به عدد وارد کنید:")
    context.user_data['type'] = 'expense'
    return AMOUNT

# Handler for receiving amount
async def amount_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        amount = float(update.message.text.replace(',', ''))
    except ValueError:
        await update.message.reply_text("لطفاً فقط عدد وارد کنید.")
        return AMOUNT
    t_type = context.user_data.get('type')
    # store transaction
    transactions.append((user_id, amount, t_type, datetime.now()))
    await update.message.reply_text(f"{t_type} به مبلغ {amount:,} ثبت شد.", reply_markup=main_menu())
    return ConversationHandler.END

async def show_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    total_income = sum(t[1] for t in transactions if t[0] == user_id and t[2] == 'income')
    total_expense = sum(t[1] for t in transactions if t[0] == user_id and t[2] == 'expense')
    report = (
        f"📊 گزارش مالی شما:\n"
        f"➕ مجموع درآمدها: {total_income:,} تومان\n"
        f"➖ مجموع هزینه‌ها: {total_expense:,} تومان\n"
        f"💰 مانده حساب: {total_income - total_expense:,} تومان"
    )
    # budget info
    if budgets.get(user_id):
        b = budgets[user_id]
        report += f"\n\n📌 بودجه ماهانه: {b:,} تومان"
        report += f"\n➖ باقی‌مانده بودجه: {b - total_expense:,} تومان"
    await update.message.reply_text(report)

async def set_budget_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفاً مبلغ بودجه ماهانه را وارد کنید:")
    return AMOUNT

async def budget_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        amount = float(update.message.text.replace(',', ''))
    except ValueError:
        await update.message.reply_text("لطفاً فقط عدد وارد کنید.")
        return AMOUNT
    budgets[user_id] = amount
    await update.message.reply_text(f"بودجه ماهانه {amount:,} تومان تنظیم شد.", reply_markup=main_menu())
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("عملیات کنسل شد.", reply_markup=main_menu())
    return ConversationHandler.END


def main_menu():
    return ReplyKeyboardMarkup(
        [['📊 گزارش', '➕ درآمد'], ['➖ هزینه', '💰 تنظیم بودجه']],
        resize_keyboard=True
    )
