import telebot

TOKEN = '1119831121:AAHb_nvYn1M5NciLJu1NX-48jMTkrPUZ0sc'

CHAT_ID = 'https://t.me/hello_min'

from apscheduler.schedulers.background import BackgroundScheduler

def send_message(event, context):
    bot = telegram.Bot(token=TOKEN)
    bot.sendMessage(chat_id = CHAT_ID, text = 'Daily reminder has been set! You\'ll get notified at 11 AM daily')

sched = BackgroundScheduler()

# Runs from Monday to Friday at 11:30 (am) until 2014-07-30 00:00:00
sched.add_job(send_message, 'cron', day_of_week='mon-fri', hour=11, minute=30, end_date='2021-07-30')

sched.start()


