import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from main_menu import get_main_menu

CAR_SELECT = 0

car_names = [
    "FOTON AUMARK S",
    "FOTON TRUCK MATE 1",
    "FOTON TRUCK MATE 2",
    "FOTON MILER",
    "FOTON TUNLAND G7",
    "FOTON TUNLAND V9",
    "FOTON VIEW CS2"
]

cars = {
    "FOTON AUMARK S": "*FOTON AUMARK S*\n"
                      "🛻 Yil: 2025\n"
                      "⚙️ Dvigatel: 2.8L Turbo Diesel\n"
                      "⚖️ Yuk ko‘tarish: 5 tonna\n"
                      "💸 Narx: 375 088 000 so‘m",

    "FOTON TRUCK MATE 1": "*FOTON TRUCK MATE 1*\n"
                          "🛻 Yil: 2025\n"
                          "⚙️ Dvigatel: 1.6L Benzin\n"
                          "⚖️ Yuk ko‘tarish: 1.2 tonna\n"
                          "💸 Narx: 175 840 000 so‘m",

    "FOTON TRUCK MATE 2": "*FOTON TRUCK MATE 2*\n"
                          "🛻 Yil: 2024\n"
                          "⚙️ Dvigatel: 2.0L Benzin\n"
                          "⚖️ Yuk ko‘tarish: 1.5 tonna\n"
                          "💸 Narx: 205 000 000 so‘m",

    "FOTON MILER": "*FOTON MILER*\n"
                   "🛻 Yil: 2024\n"
                   "⚙️ Dvigatel: 2.2L Turbo Diesel\n"
                   "⚖️ Yuk ko‘tarish: 3.0 tonna\n"
                   "💸 Narx: 250 096 000 so‘m",

    "FOTON TUNLAND G7": "*FOTON TUNLAND G7*\n"
                        "🚙 Pikap\n"
                        "⚙️ 2.0L Turbo Diesel, 4x4\n"
                        "🪑 5 o‘rinli, ABS, ESP\n"
                        "💸 Narx: 385 056 000 so‘m",

    "FOTON TUNLAND V9": "*FOTON TUNLAND V9*\n"
                        "🚙 Pikap\n"
                        "⚙️ 2.0L Turbo Diesel, 8AT, 4WD\n"
                        "🛡️ Havfsizlik: 6 ta airbag, ESP\n"
                        "💸 Narx: 465 024 000 so‘m",

    "FOTON VIEW CS2": "*FOTON VIEW CS2*\n"
                      "🚌 15 o‘rinli mikroavtobus\n"
                      "⚙️ 2.4L Benzin, 5MT\n"
                      "👨‍👩‍👧‍👦 Maxsus yo‘lovchi tashish uchun\n"
                      "💸 Narx: 449 120 000 so‘m"
}

async def car_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[KeyboardButton(name)] for name in car_names]
    buttons.append([KeyboardButton("🔙 Orqaga")])
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("🚘 Qaysi avtomobil haqida ma'lumot kerak?", reply_markup=markup)
    return CAR_SELECT

async def car_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🔙 Orqaga":
        await update.message.reply_text("🏠 Asosiy menyu:", reply_markup=get_main_menu())
        return ConversationHandler.END

    info = cars.get(text, "Kechirasiz, bu avtomobil haqida ma'lumot topilmadi.")
    filename = text.lower().replace(" ", "_").replace("foton_", "") + ".jpg"
    path = f"images/{filename}"

    try:
        with open(path, "rb") as photo:
            await update.message.reply_photo(photo=photo, caption=info, parse_mode="Markdown")
    except FileNotFoundError:
        logging.error(f"Image file not found: {path}")
        await update.message.reply_text(info, parse_mode="Markdown")

    return CAR_SELECT

car_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^🚗 Avtomobillar"), car_start)],
    states={
        CAR_SELECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, car_selected)]
    },
    fallbacks=[]
)
