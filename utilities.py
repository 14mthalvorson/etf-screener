def to_number(value):
    value = str(value)
    if value[-1:] == 'B':
        return float(value[:-1]) * 1000000000
    elif value[-1:] == 'M':
        return float(value[:-1]) * 1000000
    elif value[-1:] == 'K':
        return float(value[:-1]) * 1000
    elif value[-1:] == "%":
        return float(value[:-1]) / 100
    else:
        return float(value)


def to_billions_string(value):
    return '{:.2f}'.format(value / 1000000000) + 'B'


def to_millions_string(value):
    return '{:.2f}'.format(value / 1000000) + 'M'


def to_thousands_string(value):
    return '{:.2f}'.format(value / 1000) + 'K'


def to_percent_string(value):
    return '{:.2f}'.format(value * 100) + '%'


# Round to nearest hundredths
def to_ratio_string(value):
    return '{:.2f}'.format(value)


# Returns median (lower num if multiple)
def get_median_from_list(vals):
    vals.sort(key=lambda x: to_number(x))
    return vals[len(vals)//2]


def clean_tickers():
    with open('input.txt', 'r+') as f:
        data = f.read()
        for string in ['Stock', 'ETF', '\t', '\n']:
            while string in data:
                data = data.replace(string, ' ')
        while '  ' in data:
            data = data.replace('  ', ' ')
        data = data.lower()
        data = ''.join([x for x in data if x in ' abcdefghijklmnopqrstuvwxyz'])
        data.strip()
        data = data.split(' ')
        data = list(set(data))
        data.sort()
        data = [x for x in data if x != '']
        data = ' '.join(data)

        with open('output.txt', 'w+') as g:
            g.write(data)
