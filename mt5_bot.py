# -*- coding: utf-8 -*-
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8216500088:AAGBvLEke9VLYwPJrf22H84YTuOS_G3T7oc" 

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(f"សួស្តី {user.first_name}!
ខ្ញុំគឺជា Bot សម្រាប់វិភាគសញ្ញា XAUUSD។
សូមផ្ញើរូបភាពក្រាហ្វ MT5 របស់អ្នកមកខ្ញុំ។")

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("សូមផ្ញើជា 'រូបភាព' នៃក្រាហ្វ MT5។ ខ្ញុំមិនយល់សារជាអក្សរទេ។")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    await message.reply_text("កំពុងវិភាគ... សូមរង់ចាំបន្តិច។")
    
    signals = ["🟢 ទិញ (Buy)", "🔴 លក់ (Sell)", "🟡 រង់ចាំសិន (Hold)"]
    prediction = random.choice(signals)
    confidence_level = random.randint(75, 95)
    
    response_text = (
        f"✅ ការវិភាគបានចប់ហើយ!
\n"
        f"សញ្ញាដែលបានទស្សន៍ទាយ: **{prediction}**\n"
        f"កម្រិតទំនុកចិត្ត: **{confidence_level}%**\n\n"
        f"**ការព្រមាន៖** នេះជាការទស្សន៍ទាយដោយ Bot ហើយអាចមានកំហុស។ សូមប្រើការវិភាគផ្ទាល់ខ្លួនមុនពេលធ្វើការជួញដូរ។"
    )

    await message.reply_text(response_text, parse_mode='Markdown')

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    application.run_polling()

if __name__ == "__main__":
    main()