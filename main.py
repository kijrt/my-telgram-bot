import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

user_watchlist = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я отслеживаю криптомонеты. Используй команды:\n"
                                      "/add BTC — добавить монету\n"
                                      "/list — показать монеты\n"
                                      "/signal BTC — получить сигнал")

@bot.message_handler(commands=['add'])
def add_coin(message):
    try:
        _, coin = message.text.split()
        user_id = message.from_user.id
        user_watchlist.setdefault(user_id, []).append(coin.upper())
        bot.reply_to(message, f"✅ Монета {coin.upper()} добавлена в список.")
    except:
        bot.reply_to(message, "⚠ Используй формат: /add BTC")

@bot.message_handler(commands=['list'])
def list_coins(message):
    user_id = message.from_user.id
    coins = user_watchlist.get(user_id, [])
    if coins:
        bot.reply_to(message, "🪙 Твои монеты: " + ", ".join(coins))
    else:
        bot.reply_to(message, "Список монет пуст. Добавь с помощью /add BTC")

@bot.message_handler(commands=['signal'])
def handle_signal(message):
    try:
        _, coin = message.text.split()
        coin = coin.upper()
        bot.reply_to(message, f"📊 Сигнал для {coin}:\n...")
    except:
        bot.reply_to(message, "⚠ Используй формат: /signal BTC")

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.reply_to(message, "Я не понимаю. Используй команды: /add, /list, /signal")

bot.polling()
