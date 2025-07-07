from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, filters, ContextTypes
from main_menu import get_main_menu  # bu sizning asosiy menyu faylingizdan

CREDIT_PRICE, CREDIT_PREPAY, CREDIT_MONTH = range(3)

# 🔁 Har bir bosqich uchun orqaga tugmasi
back_button = ReplyKeyboardMarkup([["🔙 Orqaga"]], resize_keyboard=True)

async def credit_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("\U0001F4B0 Avtomobil narxini kiriting (so'mda):", reply_markup=back_button)
    return CREDIT_PRICE

async def credit_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        return await cancel(update, context)
    try:
        price = int(update.message.text.replace(" ", ""))
        context.user_data["price"] = price
        await update.message.reply_text("\U0001F4B5 Boshlang‘ich to‘lovni kiriting (foizda, masalan: 30):", reply_markup=back_button)
        return CREDIT_PREPAY
    except ValueError:
        await update.message.reply_text("\u2757 Raqam kiriting.", reply_markup=back_button)
        return CREDIT_PRICE

async def credit_prepay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        return await cancel(update, context)
    try:
        percent = float(update.message.text)
        price = context.user_data["price"]
        prepayment = price * percent / 100
        context.user_data["prepayment"] = prepayment
        await update.message.reply_text("\U0001F4C6 To‘lov muddatini kiriting (oyda, masalan: 24):", reply_markup=back_button)
        return CREDIT_MONTH
    except ValueError:
        await update.message.reply_text("\u2757 Foizni to‘g‘ri kiriting.", reply_markup=back_button)
        return CREDIT_PREPAY

async def credit_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 Orqaga":
        return await cancel(update, context)
    try:
        months = int(update.message.text)
        price = context.user_data["price"]
        prepayment = context.user_data["prepayment"]
        loan_amount = price - prepayment

        annual_rate = 26
        monthly_rate = annual_rate / 12 / 100
        insurance = loan_amount * 0.009 * (months // 12)

        if monthly_rate == 0:
            monthly_payment = loan_amount / months
        else:
            monthly_payment = loan_amount * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)

        total_payment = monthly_payment * months + insurance

        msg = (
            f"\U0001F4CA *Kredit hisob-kitobi:*\n"
            f"\U0001F4B5 Avtomobil narxi: {price:,.0f} so'm\n"
            f"\u2B07 Boshlang‘ich to‘lov: {prepayment:,.0f} so'm\n"
            f"\U0001F4C8 Qarz: {loan_amount:,.0f} so'm\n"
            f"\U0001F6E1 Sug‘urta ({months // 12} yil): {insurance:,.0f} so'm\n"
            f"\U0001F4C6 Muddat: {months} oy\n"
            f"\U0001F4CA Yillik stavka: {annual_rate}%\n"
            f"\U0001F4B3 Oylik to‘lov: {monthly_payment:,.0f} so'm\n"
            f"\U0001F4B0 Umumiy to‘lov: {total_payment:,.0f} so'm"
        )
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=get_main_menu())
        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text("\u2757 Oy sonini to‘g‘ri kiriting.", reply_markup=back_button)
        return CREDIT_MONTH

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("\u274C Bekor qilindi.", reply_markup=get_main_menu())
    return ConversationHandler.END

credit_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^💳 Kredit kalkulyator$"), credit_start)],
    states={
        CREDIT_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, credit_price)],
        CREDIT_PREPAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, credit_prepay)],
        CREDIT_MONTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, credit_month)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        MessageHandler(filters.Regex("^🔙 Orqaga$"), cancel),
    ]
)
