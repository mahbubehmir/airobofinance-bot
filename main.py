from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers import start, record_income, record_expense, show_report, set_budget

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^📊 گزارش$"), show_report))
    app.add_handler(MessageHandler(filters.Regex("^➕ درآمد$"), record_income))
    app.add_handler(MessageHandler(filters.Regex("^➖ هزینه$"), record_expense))
    app.add_handler(MessageHandler(filters.Regex("^💰 تنظیم بودجه$"), set_budget))

    app.run_polling()

if __name__ == "__main__":
    main()
