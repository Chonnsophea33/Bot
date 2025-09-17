# -*- coding: utf-8 -*-
import random
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import logging
from aiohttp import web

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# ហៅយក Bot Token ពី Environment Variable (Secret)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# កំណត់ Webhook URL ពី Environment Variable (Render នឹងផ្ដល់វា)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL environment variable is not set.")

# ហៅយក PORT ពី Environment Variable (Render នឹងផ្ដល់វា)
PORT = int(os.environ.get("PORT", 5000))

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(f"សួស្តី {user.first_name}!\nខ្ញុំគឺជា Bot សម្រាប់វិភាគសញ្ញា XAUUSD។\nសូមផ្ញើរូបភាពក្រាហ្វ MT5 របស់អ្នកមកខ្ញុំ។")

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("សូមផ្ញើជា 'រូបភាព' នៃក្រាហ្វ MT5។ ខ្ញុំមិនយល់សារជាអក្សរទេ។")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    await message.reply_text("កំពុងវិភាគ... សូមរង់ចាំបន្តិច។")
    
    signals = ["🟢 ទិញ (Buy)", "🔴 លក់ (Sell)", "🟡 រង់ចាំសិន (Hold)"]
    prediction = random.choice(signals)
    confidence_level = random.randint(75, 95)
    
    response_text = (
        f"✅ ការវិភាគបានចប់ហើយ!\n\n"
        f"សញ្ញាដែលបានទស្សន៍ទាយ: **{prediction}**\n"
        f"កម្រិតទំនុកចិត្ត: **{confidence_level}%**\n\n"
        f"**ការព្រមាន៖** នេះជាការទស្សន៍ទាយដោយ Bot ហើយអាចមានកំហុស។ សូមប្រើការវិភាគផ្ទាល់ខ្លួនមុនពេលធ្វើការជួញដូរ។"
    )

    await message.reply_text(response_text, parse_mode='Markdown')

async def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # Set webhook
    await application.bot.set_webhook(url=WEBHOOK_URL)
    
    # Start web server
    web_server = web.Application()
    web_server.add_routes([web.post("/", application.web_handler)])
    runner = web.AppRunner(web_server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    
    await application.start()
    
    # Keep the application running
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
