from finviz_finance_fulfillment import *


class Ticker:

    def __init__(self, ticker):
        self.ticker = ticker

        fundamentals = get_finviz_metrics(ticker, ['Company', 'Price', 'Market Cap', 'Sales', 'Dividend %', 'P/E', 'P/S',
                                                 'EPS this Y', 'Sales Q/Q', 'Sales past 5Y', 'Gross Margin',
                                                 'Oper. Margin', 'Profit Margin', 'SMA200', '52W High', '52W Low',
                                                 'Perf Year'])

        self.company = fundamentals['Company']
        self.price = fundamentals['Price']
        self.market_cap = fundamentals['Market Cap']
        self.revenue = fundamentals['Sales']
        self.dividend_yield = fundamentals['Dividend %']
        self.pe_ratio = fundamentals['P/E']
        self.ps_ratio = fundamentals['P/S']
        self.eps_this_y = fundamentals['EPS this Y']
        self.revenue_growth = fundamentals['Sales Q/Q']
        self.revenue_growth_5y = fundamentals['Sales past 5Y']
        self.gross_margin = fundamentals['Gross Margin']
        self.operating_margin = fundamentals['Oper. Margin']
        self.profit_margin = fundamentals['Profit Margin']
        self.sma200 = fundamentals['SMA200']
        self.high_52W = fundamentals['52W High']
        self.low_52W = fundamentals['52W Low']
        self.perf_year = fundamentals['Perf Year']

        try:
            self.gross_income = '{:.2f}'.format(float(self.gross_margin[:-1]) / 100 * float(self.revenue[:-1])) + 'B'
        except Exception:
            print('Could not calculate Gross Income for', self.ticker)

        try:
            self.operating_income = '{:.2f}'.format(float(self.operating_margin[:-1]) / 100 * float(self.revenue[:-1])) + 'B'
        except Exception:
            print('Could not calculate Operating Income for', self.ticker)
