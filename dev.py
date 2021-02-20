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
        res = (p_out - p_in) * count * 0.997
    else:
        res = (p_in - p_out) * count * 0.997

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
