from telegram import (
    KeyboardButton, ReplyKeyboardMarkup,
    InlineKeyboardMarkup, InlineKeyboardButton,
    Update
)
from telegram.ext import (
    ContextTypes, ConversationHandler,
    MessageHandler, CallbackQueryHandler,
    CommandHandler, filters
)
from datetime import datetime, timedelta
from main_menu import get_main_menu

# Bosqichlar
TEST_CAR, TEST_PHONE, TEST_DATE, TEST_TIME = range(4)

# Avtomobillar
test_cars = [
    "FOTON AUMARK S",
    "FOTON TRUCK MATE 1",
    "FOTON TRUCK MATE 2",
    "FOTON MILER",
    "FOTON TUNLAND G7",
    "FOTON TUNLAND V9",
    "FOTON VIEW CS2"
]

# IDlar
ADMIN_ID = 6911557112
CHANNEL_ID = "@foton_club_1"

# --- Yonma-yon tugma generatori ---
def generate_car_buttons(cars, row_width=2):
    buttons = []
    for i in range(0, len(cars), row_width):
        row = [KeyboardButton(car) for car in cars[i:i+row_width]]
        buttons.append(row)
    buttons.append([KeyboardButton("🔙 Orqaga")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# --- Sana tanlash (inline) ---
def generate_calendar():
    today = datetime.today()
    buttons = []
    for i in range(7):
        date = today + timedelta(days=i)
        buttons.append([
            InlineKeyboardButton(
                date.strftime("%Y-%m-%d"),
                callback_data=date.strftime("%Y-%m-%d")
            )
        ])
    return InlineKeyboardMarkup(buttons)

# --- Start ---
async def testdrive_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚘 Qaysi avtomobilni test drive qilmoqchisiz?",
        reply_markup=generate_car_buttons(test_cars)
    )
    return TEST_CAR

# --- Car tanlandi ---
async def testdrive_car(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🔙 Orqaga":
        await update.message.reply_text("🏠 Asosiy menyu:", reply_markup=get_main_menu())
        return ConversationHandler.END

    if text not in test_cars:
        await update.message.reply_text("❌ Noto‘g‘ri tanlov. Iltimos, tugmalardan birini tanlang.")
        return TEST_CAR

    context.user_data["car"] = text

    contact_btn = KeyboardButton("📾 Telefon raqamni yuborish", request_contact=True)
    markup = ReplyKeyboardMarkup([[contact_btn], [KeyboardButton("🔙 Orqaga")]], resize_keyboard=True)
    await update.message.reply_text("📲 Iltimos, telefon raqamingizni yuboring:", reply_markup=markup)
    return TEST_PHONE

# --- Telefon ---
async def testdrive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        return await testdrive_start(update, context)

    contact = update.message.contact
    if not contact:
        await update.message.reply_text("❗ Iltimos, telefon raqamni tugma orqali yuboring.")
        return TEST_PHONE

    context.user_data["phone"] = contact.phone_number

    await update.message.reply_text(
        "🗕 Test drive uchun sanani tanlang:",
        reply_markup=generate_calendar()
    )
    return TEST_DATE

# --- Sana ---
async def testdrive_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["date"] = query.data

    await query.edit_message_text(
        f"🕒 Tanlangan sana: {query.data}\n\nEndi vaqtni yozing (masalan: 14:00)"
    )
    return TEST_TIME

# --- Vaqt ---
async def testdrive_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        await update.message.reply_text(
            "🗕 Iltimos, qaytadan sanani tanlang:",
            reply_markup=generate_calendar()
        )
        return TEST_DATE

    user = update.message.from_user
    car = context.user_data.get("car", "Noma’lum")
    phone = context.user_data.get("phone", "Noma’lum")
    date = context.user_data.get("date", "Noma’lum")
    time = update.message.text

    username = f"@{user.username}" if user.username else "yo‘q"

    msg = (
        f"🧪 *Test drive so‘rovi!*\n"
        f"👤 Ism: {user.full_name}\n"
        f"📱 Username: {username}\n"
        f"📞 Telefon: {phone}\n"
        f"🚘 Avtomobil: {car}\n"
        f"🗓 Sana: {date}\n"
        f"🕒 Vaqt: {time}"
    )

    await update.message.reply_text(
        "✅ So‘rovingiz qabul qilindi! Tez orada bog‘lanamiz.",
        reply_markup=get_main_menu()
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="Markdown")
    await context.bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode="Markdown")

    return ConversationHandler.END

# --- Bekor qilish / fallback ---
async def testdrive_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ So‘rov bekor qilindi.", reply_markup=get_main_menu())
    return ConversationHandler.END

# --- CONVERSATION HANDLER ---
test_conv = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("^\U0001f9ea Test drive$"), testdrive_start)
    ],
    states={
        TEST_CAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, testdrive_car)],
        TEST_PHONE: [
            MessageHandler(filters.CONTACT, testdrive_phone),
            MessageHandler(filters.TEXT & ~filters.COMMAND, testdrive_phone)
        ],
        TEST_DATE: [CallbackQueryHandler(testdrive_date)],
        TEST_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, testdrive_time)],
    },
    fallbacks=[
        CommandHandler("cancel", testdrive_cancel),
        MessageHandler(filters.Regex("^\U0001f519 Orqaga$"), testdrive_cancel)
    ],
    per_message=False  # yoki butunlay olib tashlang
)