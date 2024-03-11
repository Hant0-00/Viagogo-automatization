import telebot

from ticket_tracking.models import Event

bot = telebot.TeleBot('6515402227:AAHxB2hDjHzZ9fX2jDlFRE__R0lb5yUiwA0')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello")