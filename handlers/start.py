from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CommandHandler

async def start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("🚗 Avtomobillar"), KeyboardButton("💸 Kredit")],
            [KeyboardButton("📞 Kontakt"), KeyboardButton("❓ Yordam")],
            [KeyboardButton("📩 Shikoyat"), KeyboardButton("🧪 Test drive")]  # 👈 TO‘G‘RI YOPILDI
        ],
        resize_keyboard=True
    )
    await update.message.reply_text("🏠 Asosiy menyu:", reply_markup=main_keyboard)

# start handler
start_handler = CommandHandler("start", start_menu)
