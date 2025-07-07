# handlers/contact.py

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from db import get_connection

ADMIN_ID = 6911557112
CHANNEL_ID = '@foton_club_1'

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    ism = contact.first_name + " " + (contact.last_name or "")
    tel = contact.phone_number
    tg_id = contact.user_id or update.message.from_user.id
    username = update.message.from_user.username or "yo‘q"

    # Bazaga yozish
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO kontaktlar (ism, tel, tg_id, username) VALUES (%s, %s, %s, %s)",
            (ism, tel, tg_id, username)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Bazaga yozishda xatolik:", e)

    # Admin va kanalga xabar
    msg = (
        f"📥 *Yangi kontakt!*\n"
        f"👤 Ism: {ism}\n"
        f"📞 Tel: {tel}\n"
        f"🆔 ID: {tg_id}\n"
        f"🌐 Username: @{username}"
    )

    await update.message.reply_text("✅ Kontakt qabul qilindi. Tez orada siz bilan bog‘lanamiz.")
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="Markdown")
    await context.bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode="Markdown")

# === ENTRY POINT ===
contact_conv = MessageHandler(filters.CONTACT, handle_contact)
