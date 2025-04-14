import telebot
import os
import json
import requests

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

WATCHLIST_FILE = "coins.json"

# Загрузка списка монет
def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, "r") as f:
            return json.load(f)
    return {}

# Сохранение списка монет
def save_watchlist(data):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(data, f)

user_watchlist = load_watchlist()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я отслеживаю криптомонеты. Используй команды:\n"
                                      "/add BTC — добавить монету\n"

                                      "/list — показать монеты \n"

                                      "/signal BTC — получить сигнал"
                    )

@bot.message_handler(commands=['add'])
def add_coin(message):
    try:
        _, coin = message.text.split()
        user_id = str(message.from_user.id)
        user_watchlist.setdefault(user_id, []).append(coin.upper())
        save_watchlist(user_watchlist)
        bot.reply_to(message, f"✅ Монета {coin.upper()} добавлена в список.")
    except:
        bot.reply_to(message, "⚠ Используй формат: /add BTC")

@bot.message_handler(commands=['list'])
def list_coins(message):
    user_id = str(message.from_user.id)
    coins = user_watchlist.get(user_id, [])
    if coins:
        bot.reply_to(message, "Ваши монеты:"bot.reply_to(message, f"Ваши монеты:\n{coin_list}")
" + "
".join(coins))"
    else:
        bot.reply_to(message, "У вас пока нет монет.")

@bot.message_handler(commands=['signal'])
def handle_signal(message):
    try:
        _, coin = message.text.split()
        coin = coin.upper()
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin.lower()}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        price = data.get(coin.lower(), {}).get("usd")
        if price:
            bot.reply_to(message, f"📊 Цена {coin}: {price} USD")
        else:
            bot.reply_to(message, f"❌ Не удалось найти цену для {coin}")
    except:
        bot.reply_to(message, "⚠ Используй формат: /signal BTC")

bot.polling()
