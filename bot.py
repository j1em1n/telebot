"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Deployed using heroku.

"""
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import schedule
import time
import requests
import datetime
import pytz
import os
PORT = int(os.environ.get('PORT', 5000))


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = '1119831121:AAHb_nvYn1M5NciLJu1NX-48jMTkrPUZ0sc'
HEROKU_APP_NAME = 'https://zi1ch.herokuapp.com/'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

################################################
def telegram_bot_sendtext(bot_message):
    bot_token = '1119831121:AAHb_nvYn1M5NciLJu1NX-48jMTkrPUZ0sc'
    bot_chatID = '@hello_min'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response

# time.strftime('%X %x %Z')
os.environ['TZ'] = 'Asia/Singapore'
time.tzset()
hour_minute = '13:00'
hour_minute1 ='14:20'

test = telegram_bot_sendtext("i am a bot!")
# print(test)
# schedule.every(10).seconds.do(test)
schedule.every().day.at(hour_minute).do(test)
schedule.every().day.at(hour_minute1).do(test)

while True:
    schedule.run_pending()
    time.sleep(1)

################################################
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))


    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://zi1ch.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()