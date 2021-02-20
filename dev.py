def income(count, p_in, p_out):
    """
    прибыль при игре на повышении или на понижении
    :param count: кол-во акций
    :param p_in: цена покупки
    :param p_out: цена продажи
    :return:
    """
    res = 0
    if p_out >= p_in:
        res = (p_out - p_in - p_out * 0.003 - p_in * 0.003) * count
    else:
        res = (p_in - p_out - p_out * 0.003 - p_in * 0.003) * count

    return round(res * 0.87 if res > 0 else res, 3)


def lose(count, p_in, p_out):
    """
    убыток при продаже акций по более низкой цене
    :param count: кол-во акций
    :param p_in: цена покупки
    :param p_out: цена продажи
    :return:
    """
    return round(p_in - p_out - p_in * 0.003 - p_out * 0.003, 3)


def price_out(count, p_in, profit):
    """
    сколько должна стоит акция для достижения профита
    :param count: кол-во акций
    :param p_in: цена акции
    :param profit: профит
    :return:
    """
    return {'up': round((profit / 0.87 + (count * p_in * 1.003)) / (count * 0.997), 3),
            'down': round(((count * p_in * 0.997) - profit/0.87) / (count * 1.003), 3)}
