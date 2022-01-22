from macrotrends_fulfillment import *
from yfinance_fulfillment import *
from utilities import *


class Stock:

    def __init__(self, ticker):
        self.ticker = ticker

        finviz_fundamentals = get_finviz_metrics(ticker, ['Company', 'Price', 'Market Cap', 'Sales', 'Dividend %', 'P/E', 'P/S',
                                                 'EPS this Y', 'Sales Q/Q', 'Sales past 5Y', 'Gross Margin',
                                                 'Oper. Margin', 'Profit Margin', 'Beta', 'SMA200', '52W High', '52W Low',
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
        self.med_rev_growth_3y = get_macrotrends_metrics(ticker, 'Median Rev Growth 3Y')
        self.ebitda_growth_3y = get_macrotrends_metrics(ticker, 'EBITDA past 3Y')
        self.gross_margin = finviz_fundamentals['Gross Margin']
        self.operating_margin = finviz_fundamentals['Oper. Margin']
        self.max_operating_margin_3y = get_macrotrends_metrics(ticker, 'Max Operating Margin 3Y')
        self.profit_margin = finviz_fundamentals['Profit Margin']
        self.beta = finviz_fundamentals['Beta']
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

        # Value checks
        if self.revenue == '-':
            self.revenue = None

        # Gross profit
        try:
            self.gross_profit = to_billions_string(to_number(self.gross_margin) * to_number(self.revenue))
        except Exception as e:
            self.gross_profit = None

        # Operating income
        try:
            self.operating_income = to_billions_string(to_number(self.operating_margin) * to_number(self.revenue))
        except Exception as e:
            self.operating_income = None

        # Adjusted operating income: max op margin 3y * current revenue
        try:
            self.adj_operating_income = to_billions_string(to_number(self.max_operating_margin_3y) * to_number(self.revenue))
        except Exception as e:
            self.adj_operating_income = None

        # Potential operating income: (max op margin 3y + 0.05) * current revenue
        try:
            self.pot_operating_income = to_billions_string(
                (to_number(self.max_operating_margin_3y) + 0.05) * to_number(self.revenue))
        except Exception as e:
            self.pot_operating_income = None

        # Cash
        try:
            self.cash = to_billions_string(to_number(self.market_cap) / to_number(self.pc_ratio))
        except Exception as e:
            self.cash = 0

        # Free cash flow
        try:
            self.free_cash_flow = to_billions_string(to_number(self.market_cap) / to_number(self.pfcf_ratio))
        except Exception as e:
            self.free_cash_flow = None

        # Enterprise value
        try:
            self.enterprise_value = to_billions_string(to_number(self.market_cap) + to_number(self.debt_long_term) - to_number(self.cash))
        except Exception as e:
            self.enterprise_value = self.market_cap

        # EV to EBITDA Ratio
        try:
            self.ev_to_ebitda_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.ebitda))
        except Exception as e:
            self.ev_to_ebitda_ratio = None

        # EBITDA Margin
        try:
            self.ebitda_margin = to_percent_string(to_number(self.ebitda) / to_number(self.revenue))
        except Exception as e:
            self.ebitda_margin = None

        # EV to Gross Profit Ratio
        try:
            self.ev_to_gp_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.gross_profit))
        except Exception as e:
            self.ev_to_gp_ratio = None

        # EV to Operating Profit Ratio
        try:
            self.ev_to_op_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.operating_income))
        except Exception as e:
            self.ev_to_op_ratio = None

        # Adjusted EV to Operating Profit Ratio
        try:
            self.adj_ev_to_op_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.adj_operating_income))
        except Exception as e:
            self.adj_ev_to_op_ratio = self.ev_to_op_ratio

        # EV to Potential Operating Profit Ratio
        try:
            self.ev_to_pot_op_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.pot_operating_income))
        except Exception as e:
            self.ev_to_pot_op_ratio = self.adj_ev_to_op_ratio

        # EV to Sales Ratio
        try:
            self.ev_to_sales_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.revenue))
        except Exception as e:
            self.ev_to_sales_ratio = None

        # Revenue per Employee
        try:
            self.revenue_per_employee = to_thousands_string(to_number(self.revenue) / to_number(self.employees))
        except Exception as e:
            self.revenue_per_employee = None

        # EBITDA per Employee
        try:
            self.ebitda_per_employee = to_thousands_string(to_number(self.ebitda) / to_number(self.employees))
        except Exception as e:
            self.ebitda_per_employee = None

        # Gross profit per Employee
        try:
            self.gross_profit_per_employee = to_thousands_string(to_number(self.gross_profit) / to_number(self.employees))
        except Exception as e:
            self.gross_profit_per_employee = None
