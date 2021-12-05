def to_number(value):
    if value[-1:] == 'B':
        return float(value[:-1]) * 1000000000
    elif value[-1:] == 'M':
        return float(value[:-1]) * 1000000
    elif value[-1:] == "%":
        return float(value[:-1]) / 100


def to_billions_string(value):
    return '{:.2f}'.format(value / 1000000000) + 'B'


def to_millions_string(value):
    return '{:.2f}'.format(value / 1000000) + 'M'


def to_percent_string(value):
    return '{:.2f}'.format(value * 100) + '%'
