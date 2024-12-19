import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = "Привет! Я бот, который поможет узнать цену валюты.\n" \
           "Чтобы узнать цену, отправьте сообщение в формате: \n" \
           "<имя валюты, цену которой хотите узнать> " \
           "<имя валюты, в которой хотите узнать цену> " \
           "<количество первой валюты>\n" \
           "Например: usd rub 10\n\n" \
           "Доступные команды:\n" \
           "/values - показать доступные валюты.\n" \
           "/help или /start - показать это сообщение."
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    text = "Доступные валюты: \nUSD - Доллар США\nEUR - Евро\nRUB - Рубль"
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def handle_convert(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Неверное количество параметров. Требуется 3 параметра.')

        base, quote, amount = values
        price = CurrencyConverter.get_price(base, quote, amount)
        bot.send_message(message.chat.id, f'Цена {amount} {base} в {quote} = {price:.2f}')
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации: {e.message}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Неизвестная ошибка: {e}")


if __name__ == '__main__':
    bot.polling(none_stop=True)