import os
import telepot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

def start_bot():
    bot = telepot.Bot(BOT_TOKEN)
    return bot

bot = start_bot()