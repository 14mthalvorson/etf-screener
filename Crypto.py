# Supports Bitcoin, Ethereum, Ripple, Litecoin
import warnings
from finvizfinance import crypto


mappings = {
    'BTCUSD': {'name': 'Bitcoin', 'line': 8},
    'ETHUSD': {'name': 'Ethereum', 'line': 10},
    'XRPUSD': {'name': 'Ripple', 'line': 9},
    'LTCUSD': {'name': 'Litecoin', 'line': 11}}


class Crypto:
    def __init__(self, ticker):

        self.ticker = ticker
        self.type = 'Crypto'

        warnings.filterwarnings('ignore')
        c = crypto.Crypto()
        df = c.performance()

        if ticker in mappings:
            data = df.iloc[mappings[ticker]['line']]
            self.name = mappings[ticker]['name']

        self.price = data['Price']
        self.perf_year = data['Perf Year']

        # Truncate price to hundredths
        if '.' in self.price:
            self.price = self.price[:self.price.index('.') + 3]

