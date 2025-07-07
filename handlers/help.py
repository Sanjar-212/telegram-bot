from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Bu bot sizga FOTON avtomobillari haqida ma'lumot beradi. Savollar bo‘lsa,@Foton_motor_Sanjarbek shu yerga yozing."
    )

help_handler = MessageHandler(filters.Regex("^❓ Yordam$"), help_command)

