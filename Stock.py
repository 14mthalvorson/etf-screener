from finviz_finance_fulfillment import *
from yfinance_fulfillment import *
from utilities import *


class Stock:

    def __init__(self, ticker):
        self.ticker = ticker

        finviz_fundamentals = get_finviz_metrics(ticker, ['Company', 'Price', 'Market Cap', 'Sales', 'Dividend %', 'P/E', 'P/S',
                                                 'EPS this Y', 'Sales Q/Q', 'Sales past 5Y', 'Gross Margin',
                                                 'Oper. Margin', 'Profit Margin', 'SMA200', '52W High', '52W Low',
                                                 'Perf Year', 'Shs Outstand', 'P/C', 'P/FCF'])

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
        self.shares = finviz_fundamentals['Shs Outstand']
        self.pc_ratio = finviz_fundamentals['P/C']  # price/cash ratio
        self.pfcf_ratio = finviz_fundamentals['P/FCF']  # price/free cash flow

        self.gross_income = None
        self.operating_income = None
        self.cash = None
        self.free_cash_flow = None

        # Gross income
        try:
            self.gross_income = to_billions_string(to_number(self.gross_margin) * to_number(self.revenue))
        except Exception as e:
            print(e)

        # Operating income
        try:
            self.operating_income = to_billions_string(to_number(self.operating_margin) * to_number(self.revenue))
        except Exception as e:
            print(e)

        # Cash
        try:
            self.cash = to_billions_string(to_number(self.market_cap) / to_number(self.pc_ratio))
        except Exception as e:
            print(e)

        # Free cash flow
        try:
            self.free_cash_flow = to_billions_string(to_number(self.market_cap) / to_number(self.pfcf_ratio))
        except Exception as e:
            print(e)
