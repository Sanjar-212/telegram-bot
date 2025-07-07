# handlers/location.py
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler,
    MessageHandler, filters
)
from main_menu import get_main_menu

LOCATION_SELECT = 0

async def location_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [KeyboardButton("📍 Asosiy ofis")],
        [KeyboardButton("🏢 Filial 1")],
        [KeyboardButton("🔙 Orqaga")]
    ]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("📍 Qaysi manzil kerak?", reply_markup=markup)
    return LOCATION_SELECT

async def location_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📍 Asosiy ofis":
        await update.message.reply_location(latitude=41.18766312790497, longitude=69.19514768385277)
        await update.message.reply_text("📍 Asosiy ofis: Toshkent, Yangihayot t., Xalqaro yo‘l 120. AutoSalon FOTON.")

    elif text == "🏢 Filial 1":
        await update.message.reply_location(latitude=41.2995, longitude=69.2401)
        await update.message.reply_text("🏢 Filial 1: Toshkent, Chilonzor, Muqimiy ko‘chasi 45.")

    elif text == "🔙 Orqaga":
        await update.message.reply_text("🏠 Asosiy menyu:", reply_markup=get_main_menu())
        return ConversationHandler.END

    return LOCATION_SELECT

# Export qilingan handler
location_conv = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("^📍 Manzil"), location_start)
    ],
    states={
        LOCATION_SELECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, location_selected)]
    },
    fallbacks=[]
)
