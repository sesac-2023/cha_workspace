from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

with open('./secret', 'r') as f:
    secret = {l.split('=')[0]: l.split('=')[1].strip() for l in f.readlines()}

token = secret['TELEGRAM_TOKEN']
# chat_id = secret['CHAT_ID']

async def chat_id_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.chat_id)
    await update.message.reply_text("check finished")


app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("chat_id", chat_id_check))

if __name__ == '__main__':
    print(token)
    app.run_polling()