import logging
import os
import random
import sys
import telebot
from apscheduler.schedulers.background import BackgroundScheduler

TOKEN = '1119831121:AAHb_nvYn1M5NciLJu1NX-48jMTkrPUZ0sc'
CHAT_ID = 'https://t.me/hello_min'
HEROKU_APP_NAME = 'https://ou7is.herokuapp.com/'

from telegram.ext import Updater, CommandHandler

# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE")
TOKEN = os.getenv(TOKEN)
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get(HEROKU_APP_NAME)
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://ou7is.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def start_handler(bot, update):
    # Creating a handler-function for /start command 
    logger.info("User {} started bot".format(update.effective_user["id"]))
    update.message.reply_text("Hello from Python!\nPress /random to get random number")


def random_handler(bot, update):
    # Creating a handler-function for /random command
    number = random.randint(0, 10)
    logger.info("User {} randomed number {}".format(update.effective_user["id"], number))
    update.message.reply_text("Random number: {}".format(number))

def send_message(bot):
    bot = telegram.Bot(token=TOKEN)
    bot.sendMessage(chat_id = CHAT_ID, text = 'Daily reminder has been set! You\'ll get notified at 11 AM daily')

sched = BackgroundScheduler()

# Runs from Monday to Friday at 11:30 (am) until 2014-07-30 00:00:00
sched.add_job(send_message, 'cron', day_of_week='mon-fri', hour=11, minute=30, end_date='2021-07-30')

sched.start()


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("random", random_handler))

    run(updater)
    
########################


