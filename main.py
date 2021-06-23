import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from apscheduler.schedulers.blocking import BlockingScheduler
import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = '1119831121:AAHb_nvYn1M5NciLJu1NX-48jMTkrPUZ0sc'
CHAT_ID = '474164495'
HEROKU_APP_NAME = 'https://zi1ch.herokuapp.com/'

import telebot     #edit this line
from bs4 import BeautifulSoup     #edit this line
import requests

TOKEN = "1119831121:AAHb_nvYn1M5NciLJu1NX-48jMTkrPUZ0sc"  #paste the API token from BotFather inside the inverted commas

bot = Updater(TOKEN, use_context=True)
stocks = []

@bot.message_handler(commands=["start"])
def start_message(message):
    #add a reply to the user here
    bot.send_message(message.chat.id,"Hello there! I am a bot! Ready to monitor your favorite stocks?")

@bot.message_handler(commands=["add"])
def add_stocks(message):   
    stockToAdd = message.text.strip().split(" ")
    #the line below checks the website to see if the stock exists. If it exists, then we will add it into a list for them. If not, we will tell the user that the code is invalid. 
    validityCheck = requests.get(f"https://sg.finance.yahoo.com/quote/{stockToAdd[1]}/history", allow_redirects=False)    #add website URL here
    if validityCheck.status_code == 200:
        stocks.append(stockToAdd[1])
        bot.send_message(message.chat.id,f"{stockToAdd[1]} added to list")
        print(stocks)
    else:
        bot.send_message(message.chat.id,"Wrong code entered. Please try again")

@bot.message_handler(commands=["getprice"])
def get_price(message):
    output_message = ""
    bot.send_message(message.chat.id,"Getting prices...")
    for stock in stocks:
        url = f"https://sg.finance.yahoo.com/quote/BABA/"       #add website URL here
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        price = soup.select("span[data-reactid*='14']")[0].text.strip()     #add the element that contains the stock price here
        timing = soup.select("span[data-reactid*='18']")[0].text.strip()    #add the element that contains the time here
        output_message += f"Price of {stock} \n${price}, {timing}\n"
    bot.send_message(message.chat.id,output_message)

bot.polling()

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
    dp.add_handler(CommandHandler("send", send))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)
    dp.get_price

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