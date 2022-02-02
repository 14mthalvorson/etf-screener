from macrotrends_fulfillment import get_macrotrends_metrics
from ETF import *
import warnings
from finvizfinance import crypto


class Crypto:
    def __init__(self, ticker):

        self.ticker = ticker
        self.type = 'Crypto'

        warnings.filterwarnings('ignore')
        c = crypto.Crypto()
        df = c.performance()

        if ticker == 'BTCUSD':
            data = df.iloc[8]
            self.name = 'Bitcoin'

        self.price = data['Price']
        self.perf_year = data['Perf Year']

        # Truncate price to hundredths
        if '.' in self.price:
            self.price = self.price[:self.price.index('.') + 3]

