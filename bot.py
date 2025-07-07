import logging
from telegram.ext import ApplicationBuilder, CommandHandler

# Handlers
from handlers.start import start_handler  # bu ishlatilmayapti, agar kerak bo'lmasa, o'chirish mumkin
from handlers.contact import contact_conv
from handlers.car import car_conv
from handlers.testdrive import test_conv
from handlers.credit import credit_conv
from handlers.help import help_handler
from handlers.location import location_conv
from handlers.complaint import complaint_conv
from main_menu import get_main_menu

# Log sozlamasi
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot tokeni
TOKEN = "7700415189:AAEZIl3MM9mdsrDCgK_OzIg4PVrI9p66XfQ"

# /start komandasi
async def start(update, context):
    logger.info("/start buyrug'i bajarildi")
    await update.message.reply_text("\U0001F3C1 Xush kelibsiz!", reply_markup=get_main_menu())

# Asosiy funksiya

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Asosiy komandalar va conversation handlerlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(help_handler)
    application.add_handler(car_conv)
    application.add_handler(test_conv)
    application.add_handler(credit_conv)
    application.add_handler(location_conv)
    application.add_handler(contact_conv)
    application.add_handler(complaint_conv)

    logger.info("Bot ishga tushdi")
    application.run_polling()

if __name__ == "__main__":
    main()
