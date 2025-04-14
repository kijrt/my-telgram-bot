
import os
import telebot
import time

TOKEN = os.getenv("BOT_TOKEN") or "ВСТАВЬ_СЮДА_СВОЙ_ТОКЕН"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Привет! Бот работает стабильно 24/7.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Ты сказал: {message.text}")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        time.sleep(5)
