import telebot
import os
import json
import requests

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "coins.json"

# Загрузка данных из файла
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Сохранение данных в файл
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Стартовые данные
user_watchlist = load_data()

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
        user_id = str(message.from_user.id)
        user_watchlist.setdefault(user_id, []).append(coin.upper())
        save_data(user_watchlist)
        bot.reply_to(message, f"✅ Монета {coin.upper()} добавлена в список.")
    except:
        bot.reply_to(message, "⚠ Используй формат: /add BTC")

@bot.message_handler(commands=['list'])
def list_coins(message):
    user_id = str(message.from_user.id)
    coins = user_watchlist.get(user_id, [])
    if coins:
        coin_list = "\n".join(coins)
        bot.reply_to(message, f"Ваши монеты:\n{coin_list}")
    else:
        bot.reply_to(message, "Список пуст. Добавь монеты командой /add")

@bot.message_handler(commands=['signal'])
def signal_coin(message):
    try:
        _, coin = message.text.split()
        coin = coin.lower()
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        price = data[coin]['usd']
        bot.reply_to(message, f"📊 Текущая цена {coin.upper()}: ${price}")
    except:
        bot.reply_to(message, "⚠ Не удалось получить данные. Проверь название монеты.")

# Заглушка
@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.reply_to(message, "Я не понимаю. Используй команды /add, /list, /signal")

bot.polling()
