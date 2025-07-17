from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    """منوی اصلی ربات"""
    return ReplyKeyboardMarkup([
        ['➕ درآمد', '➖ هزینه'],
        ['📊 گزارش', '💰 تنظیم بودجه']
    ], resize_keyboard=True)

def income_categories_keyboard():
    """کیبورد دسته‌بندی‌های درآمد"""
    categories = ["💼 حقوق", "📈 سرمایه‌گذاری", "🎁 هدیه", "🏠 اجاره", "سایر"]
    keyboard = []
    
    for i in range(0, len(categories), 2):
        row = categories[i:i+2]
        keyboard.append([InlineKeyboardButton(cat, callback_data=cat) for cat in row])
    
    return InlineKeyboardMarkup(keyboard)

def expense_categories_keyboard():
    """کیبورد دسته‌بندی‌های هزینه"""
    categories = ["🍔 غذا", "🚗 حمل‌ونقل", "🏠 مسکن", "👕 پوشاک", "💊 سلامت", "🎮 سرگرمی", "سایر"]
    keyboard = []
    
    for i in range(0, len(categories), 3):
        row = categories[i:i+3]
        keyboard.append([InlineKeyboardButton(cat, callback_data=cat) for cat in row])
    
    return InlineKeyboardMarkup(keyboard)