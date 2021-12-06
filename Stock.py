from macrotrends_fulfillment import *
from yfinance_fulfillment import *
from utilities import *



class Stock:

    def __init__(self, ticker):
        self.ticker = ticker

        finviz_fundamentals = get_finviz_metrics(ticker, ['Company', 'Price', 'Market Cap', 'Sales', 'Dividend %', 'P/E', 'P/S',
                                                 'EPS this Y', 'Sales Q/Q', 'Sales past 5Y', 'Gross Margin',
                                                 'Oper. Margin', 'Profit Margin', 'SMA200', '52W High', '52W Low',
                                                 'Perf Year', 'Shs Outstand', 'P/C', 'P/FCF', 'Debt/Eq'])

        yfinance_fundamentals = get_yfinance_metrics(ticker, ['Sales past 3Y'])

        self.company = finviz_fundamentals['Company']
        self.price = finviz_fundamentals['Price']
        self.market_cap = finviz_fundamentals['Market Cap']
        self.revenue = finviz_fundamentals['Sales']
        self.ebitda = get_macrotrends_metrics(ticker, 'EBITDA')
        self.dividend_yield = finviz_fundamentals['Dividend %']
        self.pe_ratio = finviz_fundamentals['P/E']
        self.ps_ratio = finviz_fundamentals['P/S']
        self.eps_this_y = finviz_fundamentals['EPS this Y']
        self.revenue_growth_qoq = finviz_fundamentals['Sales Q/Q']
        self.revenue_growth_yoy = get_macrotrends_metrics(ticker, 'Sales Y/Y')
        self.revenue_growth_3y = get_macrotrends_metrics(ticker, 'Sales past 3Y')
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
        self.debt_to_equity_ratio = finviz_fundamentals['Debt/Eq']  # debt/equity ratio
        self.debt_long_term = get_macrotrends_metrics(ticker, 'Long Term Debt')

        self.gross_income = None
        self.operating_income = None
        self.cash = None
        self.free_cash_flow = None

        # Gross income
        try:
            self.gross_income = to_billions_string(to_number(self.gross_margin) * to_number(self.revenue))
        except Exception as e:
            print('gross_income', e)

        # Operating income
        try:
            self.operating_income = to_billions_string(to_number(self.operating_margin) * to_number(self.revenue))
        except Exception as e:
            print('operating_income', e)

        # Cash
        try:
            self.cash = to_billions_string(to_number(self.market_cap) / to_number(self.pc_ratio))
        except Exception as e:
            print('cash', e)

        # Free cash flow
        try:
            if self.pfcf_ratio != '-':
                self.free_cash_flow = to_billions_string(to_number(self.market_cap) / to_number(self.pfcf_ratio))
        except Exception as e:
            print('free cash flow', ticker, e)

        # Enterprise value
        try:
            self.enterprise_value = to_billions_string(to_number(self.market_cap) + to_number(self.debt_long_term) - to_number(self.cash))
        except Exception as e:
            print('enterprise value', ticker, e)

        # EV to EBITDA Ratio
        try:
            self.ev_to_ebitda_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.ebitda))
        except Exception as e:
            print('enterprise value', ticker, e)

