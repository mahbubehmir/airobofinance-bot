from telegram.ext import (
    ApplicationBuilder,
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    filters
)
from config import BOT_TOKEN
from handlers import (
    start,
    record_income_start,
    record_expense_start,
    amount_received,
    show_report,
    set_budget_start,
    budget_received,
    cancel,
    AMOUNT_INCOME,
    AMOUNT_EXPENSE,
    AMOUNT_BUDGET
)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^➕ درآمد$'), record_income_start),
            MessageHandler(filters.Regex('^➖ هزینه$'), record_expense_start),
            MessageHandler(filters.Regex('^💰 تنظیم بودجه$'), set_budget_start),
        ],
        states={
            AMOUNT_INCOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount_received)],
            AMOUNT_EXPENSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount_received)],
            AMOUNT_BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, budget_received)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.Regex('^📊 گزارش$'), show_report))

    app.run_polling()

if __name__ == '__main__':
    main()
