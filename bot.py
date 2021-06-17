"""
Deployed using heroku.
"""
import requests
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import schedule

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = '1119831121:AAHb_nvYn1M5NciLJu1NX-48jMTkrPUZ0sc'
CHAT_ID = '474164495'
HEROKU_APP_NAME = 'https://ou7is.herokuapp.com/'


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
@bot.message_handler(commands=["start"])
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


@bot.message_handler(commands=["send"])
def send_message(update, context):
    update.sendMessage('@hello_min', 'Hello')
    """Echo the user message."""
    update.message.reply_text('Daily reminder has been set! You\'ll get notified at 11 AM daily')
    
    schedule.every().day.at("14:23").do(send_message)

    while True:
        schedule.run_pending()
        time.sleep(1)

@bot.message_handler(commands=["error_log"])
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

################################

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

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://ou7is.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()