# main.py
import os
import telebot
import requests

# Инициализация бота токеном из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")
bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для хранения списка монет для каждого пользователя (в памяти)
user_coins = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Привет! Я крипто-бот, помогу отслеживать цены криптовалют.\n"
        "Доступные команды:\n"
        "/add COIN - добавить монету в список\n"
        "/list - показать добавленные монеты\n"
        "/signal COIN - получить цену монеты в USD"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['add'])
def add_coin(message):
    # Разделяем текст команды на '/add' и аргумент (название монеты)
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Пожалуйста, укажи монету после /add. Например: /add bitcoin")
        return
    coin = parts[1].strip()
    if not coin:
        bot.reply_to(message, "Пожалуйста, укажи корректное название монеты.")
        return
    user_id = message.chat.id
    if user_id not in user_coins:
        user_coins[user_id] = []
    # Проверяем, не была ли монета уже добавлена (без учета регистра)
    coin_lower = coin.lower()
    if any(c.lower() == coin_lower for c in user_coins[user_id]):
        bot.reply_to(message, f"Монета {coin} уже есть в списке.")
    else:
        user_coins[user_id].append(coin)
        bot.reply_to(message, f"Монета {coin} добавлена в ваш список.")

@bot.message_handler(commands=['list'])
def list_coins(message):
    user_id = message.chat.id
    if user_id not in user_coins or len(user_coins[user_id]) == 0:
        bot.reply_to(message, "Ваш список монет пуст. Добавьте монеты командой /add.")
    else:
        coins = user_coins[user_id]
        # Формируем строку со списком монет, каждая с новой строки
        coin_list = "\n".join(coins)
        bot.reply_to(message, f"Ваши монеты:\n{coin_list}")

@bot.message_handler(commands=['signal'])
def signal_coin(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Пожалуйста, укажи монету после /signal. Например: /signal bitcoin")
        return
    coin = parts[1].strip()
    if not coin:
        bot.reply_to(message, "Пожалуйста, укажи корректное название монеты.")
        return
    coin_id = coin.lower()
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        resp = requests.get(url)
    except Exception as e:
        bot.reply_to(message, "Ошибка при подключении к CoinGecko API. Попробуйте позже.")
        return
    if resp.status_code != 200:
        bot.reply_to(message, "Ошибка при получении данных от CoinGecko. Попробуйте позже.")
        return
    data = resp.json()
    if coin_id in data and 'usd' in data[coin_id]:
        price = data[coin_id]['usd']
        bot.reply_to(message, f"Текущая цена {coin}: ${price}")
    else:
        bot.reply_to(message, f"Монета {coin} не найдена или данные недоступны.")

# Обработка всех остальных сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def default_response(message):
    bot.reply_to(message, "Я не понимаю. Используй команды /add, /list, /signal")

if __name__ == "__main__":
    bot.infinity_polling()
