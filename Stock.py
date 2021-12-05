from finviz_finance_fulfillment import *
from yfinance_fulfillment import *
from utilities import *


class Stock:

    def __init__(self, ticker):
        self.ticker = ticker

        finviz_fundamentals = get_finviz_metrics(ticker, ['Company', 'Price', 'Market Cap', 'Sales', 'Dividend %', 'P/E', 'P/S',
                                                 'EPS this Y', 'Sales Q/Q', 'Sales past 5Y', 'Gross Margin',
                                                 'Oper. Margin', 'Profit Margin', 'SMA200', '52W High', '52W Low',
                                                 'Perf Year'])

        yfinance_fundamentals = get_yfinance_metrics(ticker, ['Sales past 3Y'])

        self.company = finviz_fundamentals['Company']
        self.price = finviz_fundamentals['Price']
        self.market_cap = finviz_fundamentals['Market Cap']
        self.revenue = finviz_fundamentals['Sales']
        self.dividend_yield = finviz_fundamentals['Dividend %']
        self.pe_ratio = finviz_fundamentals['P/E']
        self.ps_ratio = finviz_fundamentals['P/S']
        self.eps_this_y = finviz_fundamentals['EPS this Y']
        self.revenue_growth = finviz_fundamentals['Sales Q/Q']
        self.revenue_growth_3y = yfinance_fundamentals['Sales past 3Y']
        self.revenue_growth_5y = finviz_fundamentals['Sales past 5Y']
        self.gross_margin = finviz_fundamentals['Gross Margin']
        self.operating_margin = finviz_fundamentals['Oper. Margin']
        self.profit_margin = finviz_fundamentals['Profit Margin']
        self.sma200 = finviz_fundamentals['SMA200']
        self.high_52W = finviz_fundamentals['52W High']
        self.low_52W = finviz_fundamentals['52W Low']
        self.perf_year = finviz_fundamentals['Perf Year']

        try:
            self.gross_income = to_billions_string(to_number(self.gross_margin) * to_number(self.revenue))
        except Exception:
            print('Could not calculate Gross Income for', self.ticker)

        try:
            self.operating_income = to_billions_string(to_number(self.operating_margin) * to_number(self.revenue))
        except Exception:
            print('Could not calculate Operating Income for', self.ticker)
