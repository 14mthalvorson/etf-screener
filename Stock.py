from macrotrends_fulfillment import *
from yfinance_fulfillment import *
from utilities import *


class Stock:

    def __init__(self, ticker):
        self.ticker = ticker

        finviz_fundamentals = get_finviz_metrics(ticker, ['Company', 'Price', 'Market Cap', 'Sales', 'Dividend %', 'P/E', 'P/S',
                                                 'EPS this Y', 'Sales Q/Q', 'Sales past 5Y', 'Gross Margin',
                                                 'Oper. Margin', 'Profit Margin', 'SMA200', '52W High', '52W Low',
                                                 'Perf Year', 'Shs Outstand', 'P/C', 'P/FCF', 'Debt/Eq', 'Employees'])

        yfinance_fundamentals = get_yfinance_metrics(ticker, ['Sales past 3Y'])

        # Basic Data Collection
        self.name = finviz_fundamentals['Company']
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
        self.ebitda_growth_3y = get_macrotrends_metrics(ticker, 'EBITDA past 3Y')
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
        self.employees = finviz_fundamentals['Employees']

        self.gross_profit = None
        self.operating_income = None
        self.cash = None
        self.free_cash_flow = None

        # Value checks
        if self.revenue == '-':
            self.revenue = None

        # Calculated Metrics
        # Gross profit
        try:
            if self.gross_margin != '-':
                self.gross_profit = to_billions_string(to_number(self.gross_margin) * to_number(self.revenue))
            else:
                self.gross_profit = None
        except Exception as e:
            print('gross_profit', e)

        # Operating income
        try:
            self.operating_income = to_billions_string(to_number(self.operating_margin) * to_number(self.revenue))
        except Exception as e:
            pass

        # Cash
        try:
            self.cash = to_billions_string(to_number(self.market_cap) / to_number(self.pc_ratio))
        except Exception as e:
            self.cash = 0

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
            self.enterprise_value = self.market_cap

        # EV to EBITDA Ratio
        try:
            if self.ebitda is not None and to_number(self.ebitda) != 0:
                self.ev_to_ebitda_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.ebitda))
            else:
                self.ev_to_ebitda_ratio = None
        except Exception as e:
            print('enterprise value/ebitda', ticker, e)

        # EBITDA Margin
        try:
            if self.ebitda is not None and to_number(self.ebitda) != 0 and self.revenue is not None:
                self.ebitda_margin = to_percent_string(to_number(self.ebitda) / to_number(self.revenue))
            else:
                self.ebitda_margin = None
        except Exception as e:
            print('ebitda margin', ticker, e)

        # EV to Gross Profit Ratio
        try:
            if self.gross_profit is not None and to_number(self.gross_profit) != 0:
                self.ev_to_gp_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.gross_profit))
            else:
                self.ev_to_gp_ratio = None
        except Exception as e:
            print('enterprise value/gross profit', ticker, e)

        # EV to Operating Profit Ratio
        try:
            if self.operating_income is not None and to_number(self.operating_income) != 0 and self.enterprise_value is not None:
                self.ev_to_op_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.operating_income))
            else:
                self.ev_to_op_ratio = None
        except Exception as e:
            print('enterprise value/operating profit', ticker, e)

        # EV to Sales Ratio
        try:
            if self.revenue is not None and to_number(self.revenue) != 0:
                self.ev_to_sales_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.revenue))
            else:
                self.ev_to_sales_ratio = None
        except Exception as e:
            print('EV to Sales Ratio', ticker, e)

        # Revenue per Employee
        try:
            if self.revenue is not None:
                self.revenue_per_employee = to_thousands_string(to_number(self.revenue) / to_number(self.employees))
            else:
                self.revenue_per_employee = None
        except Exception as e:
            print('Revenue per employee value', ticker, e)

        # EBITDA per Employee
        try:
            self.ebitda_per_employee = to_thousands_string(to_number(self.ebitda) / to_number(self.employees))
        except Exception as e:
            print('EBITDA per employee value', ticker, e)

        # Gross profit per Employee
        try:
            if self.gross_profit is not None:
                self.gross_profit_per_employee = to_thousands_string(to_number(self.gross_profit) / to_number(self.employees))
            else:
                self.gross_profit_per_employee = None
        except Exception as e:
            print('Gross profit per employee value', ticker, e)
