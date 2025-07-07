from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, CommandHandler, filters
from main_menu import get_main_menu

COMPLAINT_TEXT = range(1)

ADMIN_ID = 6911557112  # O'zingizning admin ID'ingizni yozing

async def complaint_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✍️ Shikoyatingizni yozing. ")
    return COMPLAINT_TEXT

async def complaint_receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    username = f"@{user.username}" if user.username else "yo‘q"

    msg = (
        f"📩 *Yangi shikoyat!*\n"
        f"👤 Ism: {user.full_name}\n"
        f"📱 Username: {username}\n"
        f"📝 Xabar:\n{text}"
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="Markdown")
    await update.message.reply_text("✅ Shikoyatingiz yuborildi! Rahmat.", reply_markup=get_main_menu())
    return ConversationHandler.END

async def complaint_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Shikoyat bekor qilindi.", reply_markup=get_main_menu())
    return ConversationHandler.END

complaint_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^📩 Shikoyat$"), complaint_start)],
    states={
        COMPLAINT_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_receive)]
    },
    fallbacks=[
        CommandHandler("cancel", complaint_cancel),
        MessageHandler(filters.Regex("^🔙 Orqaga$"), complaint_cancel)
    ]
)
