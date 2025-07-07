# main_menu.py
from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    buttons = [
        [KeyboardButton("🚗 Avtomobillar"), KeyboardButton("🧪 Test drive")],
        [KeyboardButton("💳 Kredit kalkulyator"), KeyboardButton("📞 Raqam qoldirish", request_contact=True)],
        [KeyboardButton("📍 Manzil"), KeyboardButton("❓ Yordam")],
        [KeyboardButton("📩 Shikoyat")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
