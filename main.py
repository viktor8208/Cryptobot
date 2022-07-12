import telebot

from config import keys, TOKEN
from extensions import APIException, Cryptoconwerter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_q(message: telebot.types.Message):
    text = "Чтобы начать работу введите следующие данные через пробел: \n "\
           "имя валюты, в какую валюту перевести, количество переводимой валюты \n" \
           "(например: доллар рубль 2). \n " \
           "Для получения списка доступных валют введите команду: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values_q(message: telebot.types.Message):
    text = "Доступные валюты для перевода"
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        values = (message.text.split(' '))
        if len(values) != 3:
            raise APIException("Введено неверное количество параметров")
        quote, base, amount = values
        print(values)
        coste_base = Cryptoconwerter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n {e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} - {coste_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
