from ETF import *
import pickle
from datetime import date


# HashMap[ticker] = (date, object)
today_str = [int(x) for x in str(date.today()).split('-')]
today = 365 * today_str[0] + 31 * today_str[1] + today_str[2]


def clear_cache():
    with open('cache.txt', 'wb+') as f:
        cache = {'mmmmm': 'nnnnn'}
        pickle.dump(cache, f)


def add_to_cache(ticker, obj):
    try:
        with open('cache.txt', 'rb') as f:
            cache = pickle.load(f)
    except Exception as e:
        cache = {}

    cache[ticker] = (today, obj)

    with open('cache.txt', 'wb+') as f:
        pickle.dump(cache, f)


def get_from_cache(ticker):
    print(ticker)
    try:
        with open('cache.txt', 'rb') as f:
            cache = pickle.load(f)
    except Exception as e:
        cache = {}

    if ticker not in cache:
        return None

    today, obj = cache[ticker]

    return obj
