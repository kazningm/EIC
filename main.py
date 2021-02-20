import telebot, dev
from telebot import types
from pycbrf import ExchangeRates
from datetime import date

TOKEN = "1684770797:AAG9LtGM1dn-rdPspXZWplQ_KuZqgPVT-YQ"
bot = telebot.TeleBot(TOKEN)

bot.set_my_commands(commands=[types.BotCommand(command='/help', description='Описание работы бота')])


@bot.message_handler(commands=['help'])
def mode(message):
    if message.text == '/help':
        with open('help.txt', 'rb') as f:
            bot.send_message(chat_id=message.chat.id, text=f.read(), parse_mode='html')


@bot.message_handler(content_types=['text'])
def send(message):
    try:
        # подсчет прибыли или убытка при вводе 3х чисел:
        # (кол-во акций, цена покупки, цена продажи)
        if len(message.text.split()) == 3 and '+' not in message.text:
            count, price_in, price_out = list(map(float, message.text.replace(',', '.').split()))
            result = dev.income(count=count, p_in=price_in, p_out=price_out)
            if price_out >= price_in:
                bot.send_message(chat_id=message.chat.id,
                                 text='Прибыль при игре на повышении: <b>' + str(result) + '</b>',
                                 parse_mode='html')
            else:
                lose_money = round((price_in - price_out + price_in*0.003 + price_in*0.003) * count, 3)
                bot.send_message(chat_id=message.chat.id,
                                 text='Прибыль при игре на понижении: <b>' + str(abs(result)) + '</b>\n'
                                      'Убыток при пониженной цене: <b>' + str(lose_money) + '</b>\n',
                                 parse_mode='html')
        # подсчет размера комиссии при вводе двух чисел:
        # (кол-во акций, цена акции)
        elif len(message.text.split()) == 2:
            count, price = list(map(float, message.text.replace(',', '.').split()))
            result = round(count * price, 3)
            kom = round(count * price * 0.003, 3)
            bot.send_message(chat_id=message.chat.id,
                             text='Стоимость акций: <b>{0}</b> \n'
                                  'Комиссия за сделку: <b>{1}</b>'.format(str(result), str(kom)),
                             parse_mode='html')
        # ввод одного числа
        # 1) перевод долларов в рубли
        # 2) расчет стоимости продажи акции чтобы выйти в 0
        elif len(message.text.split()) == 1:
            if '$' in message.text:
                usd = float(ExchangeRates(date.today())['USD'].value)
                money = float(message.text.strip('$'))
                bot.send_message(chat_id=message.chat.id,
                                 text='Курс доллара по данным ЦБРФ на ' + str(date.today()) + ': <b>' + str(round(usd, 3)) + '</b>\n'
                                      'Вывод: <b>' + str(round(money*usd, 3)) + '</b>',
                                 parse_mode='html')
            else:
                price_in = float(message.text.replace(',', '.'))
                new_price_long = round(price_in * (1 + 0.003) / (1 - 0.003), 3) # 13% налог
                new_price_short = round(price_in * (1 - 0.003) / (1 + 0.003), 3)
                bot.send_message(chat_id=message.chat.id,
                                 text='Цена акции должна быть при игре:\n на повышении: <b>{0} ({1} %)</b>\n'
                                      ' на понижении: <b>{2} ({3} %)</b>'.format(new_price_long, round(new_price_long * 100 / price_in - 100, 3),
                                                                                 new_price_short, round(new_price_short * 100 / price_in - 100, 3)),
                                 parse_mode='html')
        #
        elif len(message.text.split()) == 3 and '+' in message.text:
            count, price, profit = list(map(float, message.text.replace(',', '.').strip('+').split()))
            # цена акции при игре на повышении для достижения указанного профита
            result_up = round((profit*0.87 + count*price*1.003)/(count*1.003), 3)
            # цена акции при игре на понижении для достижения указанного профита
            result_down = round((count*price*1.003-profit*0.87)/(count*1.003), 3)
            bot.send_message(chat_id=message.chat.id,
                             text='Для достижения профита <b>%s</b>:\n'
                                  'Цена акции при игре на повышении: <b>%s</b>\n'
                                  'Цена акции при игре на понижении: <b>%s</b>' % (profit, result_up, result_down),
                             parse_mode='html')
    except Exception as e:
        print(e)


@bot.inline_handler(func=lambda query: len(query.query) > 2)
def send_query(query):
    wolf_pos = 'https://s.tcdn.co/5d5/c45/5d5c458f-3e3c-344c-aa5a-75ed839162ae/12.png'
    wolf_neg = 'https://e7.pngegg.com/pngimages/321/743/png-clipart-jordan-belfort-the-wolf-of-wall-street-youtube-film-leonardo-dicaprio-celebrities-microphone.png'
    wolf_khm = 'https://e7.pngegg.com/pngimages/874/681/png-clipart-leonardo-dicaprio-titanic-jack-dawson-actor-billy-costigan-leonardo-dicaprio-tshirt-celebrities-thumbnail.png'
    dollar = 'https://img2.freepng.ru/20180324/rse/kisspng-computer-icons-united-states-dollar-dollar-sign-do-dollar-5ab6e7e0a640e4.668921391521936352681.jpg'
    try:
        if len(query.query.split()) == 3:
            count, price_in, price_out = list(map(float, query.query.replace(',', '.').split()))
            result = dev.income(count=count, p_in=price_in, p_out=price_out)
            if price_out >= price_in:
                game_up = types.InlineQueryResultArticle(
                    id='1',
                    title='Ебагул Лео доволен' if result > 0 else 'Ебагул Лео недоволен',
                    input_message_content=types.InputTextMessageContent(message_text=query.query),
                    description='Прибыль {0} с учетом комиссий и налога'.format(result),
                    thumb_url=wolf_pos if result > 0 else wolf_neg,
                    thumb_height=48,
                    thumb_width=48
                )
                bot.answer_inline_query(inline_query_id=query.id, results=[game_up])
            else:
                game_down = types.InlineQueryResultArticle(
                    id='2',
                    title='Ебагул Лео доволен' if result > 0 else 'Ебагул Лео недоволен',
                    input_message_content=types.InputTextMessageContent(message_text=query.query),
                    description='Прибыль {0} с учетом комиссий и налога'.format(abs(result)),
                    thumb_url=wolf_pos if result > 0 else wolf_neg,
                    thumb_height=48,
                    thumb_width=48
                )
                lose_money = dev.lose(count=count, p_in=price_in, p_out=price_out)
                game_lose = types.InlineQueryResultArticle(
                    id='3',
                    title='Ебагул Лео продает в минус',
                    input_message_content=types.InputTextMessageContent(message_text=query.query),
                    description='Убыток {0} с учетом комиссий и налога'.format(lose_money),
                    thumb_url=wolf_neg,
                    thumb_height=48,
                    thumb_width=48
                )
                bot.answer_inline_query(inline_query_id=query.id, results=[game_down, game_lose])
        elif len(query.query.split() == 2):
            count, price = list(map(float, query.query.replace(',', '.').split()))
            result = round(count * price, 3)
            kom = round(count * price * 0.003, 3)
            r = types.InlineQueryResultArticle(
                id='kom',
                title='Сделка',
                input_message_content=types.InputTextMessageContent(query.query),
                description='Стоимость акций: <b>{0}</b> \n'
                            'Комиссия за сделку: <b>{1}</b>'.format(str(result), str(kom)),
                thumb_url=wolf_khm,
                thumb_height=48,
                thumb_width=48
            )
            bot.answer_inline_query(inline_query_id=query.id, results=[r])
        elif len(query.query.split()) == 1:
            if '$' in query.query:
                usd = float(ExchangeRates(date.today())['USD'].value)
                money = float(query.query.strip('$'))
                r = types.InlineQueryResultArticle(
                    id='USD',
                    title='Доллар',
                    input_message_content=types.InputTextMessageContent(query.query),
                    description='Курс доллара: ' + str( round(usd, 3)) + '\n'
                                'Вывод: ' + str(round(money * usd, 3)),
                    thumb_url=dollar,
                    thumb_width=48,
                    thumb_height=48
                )
                bot.answer_inline_query(inline_query_id=query.id, results=[r])
            else:
                price_in = float(query.query.replace(',', '.'))
                new_price_long = round(price_in * (1 + 0.003) / (1 - 0.003), 3)
                new_price_short = round(price_in * (1 - 0.003) / (1 + 0.003), 3)

                r = types.InlineQueryResultArticle(
                    id='4',
                    title='Ебагул Лео в замешательстве',
                    input_message_content=types.InputTextMessageContent(message_text=query.query),
                    description='цена при повышении:{0} ({1} %)\n'
                                'цена при понижении:{2} ({3} %)'.format(new_price_long, round(new_price_long * 100 / price_in - 100, 3),
                                                                        new_price_short, round(new_price_short * 100 / price_in - 100, 3)),
                    thumb_url=wolf_khm,
                    thumb_height=48,
                    thumb_width=48
                )
                bot.answer_inline_query(inline_query_id=query.id, results=[r])
    except Exception as e:
        print(e)

bot.polling()
