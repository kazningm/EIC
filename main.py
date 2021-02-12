import telebot
from telebot import types

TOKEN = "1684770797:AAG9LtGM1dn-rdPspXZWplQ_KuZqgPVT-YQ"
bot = telebot.TeleBot(TOKEN)


bot.set_my_commands(commands=[types.BotCommand(command='/help', description='Описание работы бота')])

@bot.message_handler(commands=['help'])
def mode(message):
    if message.text == '/help':
        msg = "Формат сообщений боту: \n\n"
        msg += "<b> 1) X Y Z </b> \n"
        msg += "<b>Результатом</b> будет прибыль с акций при продаже с учетом комиссии брокеру (0.3%) \n"
        msg += "<i>example:</i> \n"
        msg += "4 30.59 32.92 \n"
        msg += "<i>Вывод:</i> \nПрибыль при игре на повышении: <b>-0.6</b> \n\n"
        msg += "<b> 2) X </b> \n"
        msg += "<b>Результатом</b> будут минимальные цены для продажи акций при игре на понижении/повышении для компенсирования комиссии брокера 0.3% \n"
        msg += "<i>example:</i> \n"
        msg += "10 \n"
        msg += "<i>Вывод:</i> \nЦена акции должна быть при игре:\n"
        msg += "на повышении: <b>123.74 (0.602 %)</b>\n"
        msg += "на понижении: <b>122.264 (-0.598 %)</b> \n\n"
        bot.send_message(chat_id=message.chat.id, text=msg, parse_mode='html')

def inv(count: float = 0, price_in: float = 0, price_out: float = 0) -> float:
    """
    :param count: количество акций
    :param price_in: цена покупки 1 акции
    :param price_out: цена продажи 1 акции
    :return: количество денег на выходе при продаже с учетом комиссии 0.3%
    """
    kom_in, kom_out = price_in * count * 0.003, price_out * count * 0.003
    return ((price_out - price_in) if price_out >= price_in else (price_in - price_out)) * count - (kom_in + kom_out)


# print(str(inv(*list(map(float, sys.argv[1:])))))


@bot.message_handler(content_types=['text'])
def send(message):
    try:
        if len(message.text.split()) == 3:
            count, price_in, price_out = list(map(float, message.text.split()))
            result = round(inv(count, price_in, price_out), 3)
            if price_out >= price_in:
                bot.send_message(chat_id=message.chat.id,
                                 text='Прибыль при игре на повышении: <b>' + str(result) + '</b>',
                                 parse_mode='html')
            else:
                bot.send_message(chat_id=message.chat.id,
                                 text='Прибыль при игре на понижении: <b>' + str(abs(result)) + '</b>',
                                 parse_mode='html')
        elif len(message.text.split()) == 1:
            price_in = float(message.text)
            new_price_long = price_in * (1 + 0.003) / (1 - 0.003)
            new_price_short = price_in * (1 - 0.003) / (1 + 0.003)
            bot.send_message(chat_id=message.chat.id,
                             text='Цена акции должна быть при игре:\n на повышении: <b>{0} ({1} %)</b>\n'
                                  ' на понижении: <b>{2} ({3} %)</b>'.format(round(new_price_long, 3), round(new_price_long*100/price_in-100, 3),
                                     round(new_price_short, 3), round(new_price_short*100/price_in-100, 3)),
                             parse_mode='html')
    except:
        bot.send_message(chat_id=message.chat.id, text='format - КоличествоАкций ЦенаПокупки ЦенаПродажи')

@bot.inline_handler(func=lambda query: len(query.query) > 0)
def empty_query(query):
    try:
        r = types.InlineQueryResultArticle(
            id='1',
            parse_mode='Markdown',
            title="Бот \"Математика\"",
            description=query.query,
            input_message_content=types.InputTextMessageContent(
                message_text="Эх, зря я не ввёл 2 числа :(")
        )
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        print(e)

bot.polling()
