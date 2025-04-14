import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Хранилище для монет по каждому пользователю
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
def show_list(message):
    user_id = message.from_user.id
    coins = user_watchlist.get(user_id, [])
    if coins:
        bot.reply_to(message, "Ваши монеты:\n" + "\n".join(coins))
    else:
        bot.reply_to(message, "Ваш список пуст. Добавьте монеты через /add")

@bot.message_handler(commands=['signal'])
def signal_coin(message):
    try:
        _, coin = message.text.split()
 coin = coin.upper()
        # Здесь можно подключить реальный анализ или API
        bot.reply_to(message, f"📊 Сигнал для {coin}:\nПока это просто тестовый ответ.")
    except:
        bot.reply_to(message, "⚠ Используй формат: /signal BTC")

# Обработка текстовых монет напрямую (без команды)
@bot.message_handler(func=lambda message: True)
def handle_coin_text(message):
    coin = message.text.strip().upper()
    if coin.isalpha() and len(coin) <= 10:
        bot.reply_to(message, f"📊 Анализ монеты {coin}...\n(псевдоответ для теста)")
    else:
        bot.reply_to(message, "Я не понимаю. Используй команды /add, /list, /signal")

bot.polling()
