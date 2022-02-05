mappings = {
    'BTCUSD': {'name': 'Bitcoin', 'line': 8},
    'ETHUSD': {'name': 'Ethereum', 'line': 10},
    'XRPUSD': {'name': 'Ripple', 'line': 9},
    'LTCUSD': {'name': 'Litecoin', 'line': 11}}


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
        data = data.split('\n')
        for i, item in enumerate(data):
            data[i] = item.split('\t')
            for j, thing in enumerate(data[i]):
                data[i][j] = data[i][j].strip()
            data[i][1] = float(data[i][1])

        data = {a: str(round(b, 3)) + '%' for [a, b] in data}

        with open('output.txt', 'w+') as g:
            g.write(str(data).lower())


# Takes two columns of data (tickers, weights) and outputs
def clean_tickers_to_dict():
    with open('input.txt', 'r+') as f:
        data = f.read()
        data = data.lower()
        data = data.split('\n')
        for i, item in enumerate(data):
            data[i] = item.split('\t')

        data = {a: str(b) + '%' for [a, b] in data}

        with open('output.txt', 'w+') as g:
            g.write(str(data))


def clean_vanguard_tickers_to_dict():
    with open('input.txt', 'r+') as f:
        data = f.read()
        data = data.lower()
        data = data.replace('(', '\t')
        data = data.replace(')', '')
        data = data.split('\n')
        for i, item in enumerate(data):
            data[i] = item.split('\t')

        data = {b: c for [a, b, c] in data}

        with open('output.txt', 'w+') as g:
            g.write(str(data).lower())