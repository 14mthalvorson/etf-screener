from macrotrends_fulfillment import get_macrotrends_metrics
from finviz_finance_fulfillment import get_finviz_metrics
from utilities import *
from ETF import *


class Stock:
    def __init__(self, ticker):

        self.ticker = ticker
        self.type = 'Stock'

        finviz_fundamentals = get_finviz_metrics(ticker, ['Company', 'Price', 'Market Cap', 'Sales', 'Dividend %', 'P/E', 'P/S',
                                                 'EPS this Y', 'Sales Q/Q', 'Sales past 5Y', 'Gross Margin',
                                                 'Oper. Margin', 'Profit Margin', 'Beta', 'SMA200', '52W High', '52W Low',
                                                 'Perf Year', 'Shs Outstand', 'P/C', 'P/FCF', 'Debt/Eq', 'Employees'])

        if finviz_fundamentals['Market Cap'] is None:  # Probably an ETF
            self.type = 'ETF'

        # Basic Data Collection
        self.name = finviz_fundamentals['Company']
        self.price = finviz_fundamentals['Price']
        self.market_cap = finviz_fundamentals['Market Cap']
        self.shares = finviz_fundamentals['Shs Outstand']

        self.revenue = finviz_fundamentals['Sales']
        self.ebitda = get_macrotrends_metrics(ticker, 'EBITDA')

        self.pe_ratio = finviz_fundamentals['P/E']
        self.ps_ratio = finviz_fundamentals['P/S']

        self.revenue_growth_qoq = finviz_fundamentals['Sales Q/Q']
        self.revenue_growth_yoy = get_macrotrends_metrics(ticker, 'Sales Y/Y')
        self.revenue_growth_3y = get_macrotrends_metrics(ticker, 'Sales past 3Y')
        self.revenue_growth_5y = finviz_fundamentals['Sales past 5Y']
        self.med_rev_growth_3y = get_macrotrends_metrics(ticker, 'Median Rev Growth 3Y')
        self.ebitda_growth_3y = get_macrotrends_metrics(ticker, 'EBITDA past 3Y')

        self.gross_margin = finviz_fundamentals['Gross Margin']
        self.ebit_margin = finviz_fundamentals['Oper. Margin']
        self.max_ebit_margin_3y = get_macrotrends_metrics(ticker, 'Max EBIT Margin 3Y')
        self.net_margin = finviz_fundamentals['Profit Margin']

        self.cash = get_macrotrends_metrics(ticker, 'Cash')
        self.long_term_debt = get_macrotrends_metrics(ticker, 'Long Term Debt')
        self.research_development = get_macrotrends_metrics(ticker, 'Research and Development')

        self.dividend_yield = finviz_fundamentals['Dividend %']
        self.share_count_growth_3y = get_macrotrends_metrics(ticker, '% Change in Share Count 3Y')
        self.beta = finviz_fundamentals['Beta']
        self.employees = finviz_fundamentals['Employees']

        self.sma200 = finviz_fundamentals['SMA200']
        self.high_52W = finviz_fundamentals['52W High']
        self.low_52W = finviz_fundamentals['52W Low']
        self.perf_year = finviz_fundamentals['Perf Year']

        # Value checks
        if self.revenue == '-':
            self.revenue = None

        # Gross profit
        try:
            self.gross_profit = to_billions_string(to_number(self.gross_margin) * to_number(self.revenue))
        except Exception as e:
            self.gross_profit = None

        # EBIT
        try:
            self.ebit = to_billions_string(to_number(self.ebit_margin) * to_number(self.revenue))
        except Exception as e:
            self.ebit = None

        # Adjusted EBIT: max op margin 3y * current revenue
        try:
            self.adj_ebit = to_billions_string(to_number(self.max_ebit_margin_3y) * to_number(self.revenue))
        except Exception as e:
            self.adj_ebit = None

        # Net Income
        try:
            self.net_income = to_billions_string(to_number(self.net_margin) * to_number(self.revenue))
        except Exception as e:
            self.net_income = None

        # Enterprise value
        try:
            self.enterprise_value = to_billions_string(to_number(self.market_cap) + to_number(self.long_term_debt) - to_number(self.cash))
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

        # EV to EBIT Ratio
        try:
            self.ev_to_ebit_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.ebit))
        except Exception as e:
            self.ev_to_ebit_ratio = None

        # Adjusted EV to EBIT Ratio
        try:
            self.adj_ev_to_ebit_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.adj_ebit))
        except Exception as e:
            self.adj_ev_to_ebit_ratio = self.ev_to_ebit_ratio

        # Potential EV to EBIT Ratio
        try:
            self.ev_to_pot_ebit_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.adj_ebit))
        except Exception as e:
            self.ev_to_pot_ebit_ratio = self.adj_ev_to_ebit_ratio

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

        # EBIT per Employee
        try:
            self.gross_profit_per_employee = to_thousands_string(to_number(self.gross_profit) / to_number(self.employees))
        except Exception as e:
            self.gross_profit_per_employee = None

        # R&D / Revenue
        try:
            self.research_over_revenue = to_percent_string(to_number(self.research_development) / to_number(self.revenue))
        except Exception as e:
            self.research_over_revenue = None

        # Long Term Debt / EBIT: Reflects ability to pay off debt
        try:
            self.debt_to_ebit = to_ratio_string(to_number(self.long_term_debt) / to_number(self.ebit))
        except Exception as e:
            self.debt_to_ebit = None

        # Long Term Debt / EBIT: Reflects ability to pay off debt
        try:
            self.debt_to_gp = to_ratio_string(to_number(self.long_term_debt) / to_number(self.gross_profit))
        except Exception as e:
            self.debt_to_gp = None
