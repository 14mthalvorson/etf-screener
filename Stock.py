from macrotrends_fulfillment import get_macrotrends_metrics
from ETF import *
from finviz_finance_fulfillment import get_finviz_metrics


with open('morningstar.txt', 'r+') as f:
    data = f.read()
    data = data.split('\n')
    for i, line in enumerate(data):
        data[i] = data[i].split(' ')
    morningstar_FVEs = {a: b for [a, b] in data}


class Stock:
    def __init__(self, ticker):
        ticker = ticker.lower()

        self.ticker = ticker
        self.type = 'Stock'

        finviz_fundamentals = get_finviz_metrics(ticker, ['Company', 'Price', 'Market Cap', 'Sales', 'Dividend %', 'P/E', 'P/S',
                                                 'EPS this Y', 'Sales Q/Q', 'Sales past 5Y', 'Gross Margin',
                                                 'Oper. Margin', 'Profit Margin', 'Beta', 'SMA20', 'SMA50', 'SMA200', '52W High', '52W Low',
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

        self.qoq_rev_growth = finviz_fundamentals['Sales Q/Q']  # This Q revenue / Q revenue 1 year ago
        self.ttm_rev_growth = get_macrotrends_metrics(ticker, 'TTM Rev Growth')
        self.med_ttm_rev_growth_3y = get_macrotrends_metrics(ticker, 'Median TTM Rev Growth 3Y')  # TTM Revenue Growth Rate, median of up to last 13 quarters
        self.med_qoq_rev_growth_3y = get_macrotrends_metrics(ticker, 'Median Q/Q Rev Growth 3Y')  # Median Q/Q rev growth rate
        self.annualized_rev_growth_3y = get_macrotrends_metrics(ticker, 'Annualized Rev Growth 3Y')  # Annualized Revenue Growth Rate
        self.med_qoq_rev_growth_5y = get_macrotrends_metrics(ticker, 'Median Q/Q Rev Growth 5Y')
        self.annualized_rev_growth_5y = finviz_fundamentals['Sales past 5Y']

        self.ebitda_growth_3y = get_macrotrends_metrics(ticker, 'EBITDA past 3Y')

        self.gross_margin = finviz_fundamentals['Gross Margin']
        self.ebit_margin = finviz_fundamentals['Oper. Margin']
        self.max_ebit_margin = get_macrotrends_metrics(ticker, 'Max EBIT Margin 3Y')
        self.net_margin = finviz_fundamentals['Profit Margin']

        self.cash = get_macrotrends_metrics(ticker, 'Cash')
        self.long_term_debt = get_macrotrends_metrics(ticker, 'Long Term Debt')
        self.research_development = get_macrotrends_metrics(ticker, 'Research and Development')

        self.dividend_yield = finviz_fundamentals['Dividend %']
        self.share_count_growth_3y = get_macrotrends_metrics(ticker, '% Change in Share Count 3Y')
        self.beta = finviz_fundamentals['Beta']
        self.employees = finviz_fundamentals['Employees']

        self.sma20 = finviz_fundamentals['SMA20']
        self.sma50 = finviz_fundamentals['SMA50']
        self.sma200 = finviz_fundamentals['SMA200']
        self.high_52W = finviz_fundamentals['52W High']
        self.low_52W = finviz_fundamentals['52W Low']
        self.perf_year = finviz_fundamentals['Perf Year']

        self.morningstar_FVE = morningstar_FVEs.get(ticker, None)

        # Value checks
        if self.revenue == '-':
            self.revenue = None

        if self.med_ttm_rev_growth_3y is not None and to_number(self.med_ttm_rev_growth_3y) < -0.25:
            self.med_ttm_rev_growth_3y = None

        # Adjusted Revenue Growth 3Y
        # Averages a lot of revenue growth rate metrics
        # 1 year: Q/Q, TTM
        # 3 year: Annualized, Median TTM, Median Q/Q
        # 5 year: Annualized
        try:
            revs = []
            for var in [self.qoq_rev_growth, self.ttm_rev_growth, self.med_qoq_rev_growth_3y, self.med_ttm_rev_growth_3y, self.annualized_rev_growth_3y, self.med_qoq_rev_growth_5y, self.annualized_rev_growth_5y]:
                if var is not None:
                    revs.append(var)
            revs.sort(key=lambda x: to_number(x))
            self.adj_rev_growth_3y = revs[len(revs) // 2]
            if to_number(self.adj_rev_growth_3y) > 2.00 or to_number(self.adj_rev_growth_3y) < -0.20:  # Cap max growth to 200%, min growth to -20%
                self.adj_rev_growth_3y = None
        except Exception as e:
            self.adj_rev_growth_3y = self.annualized_rev_growth_3y

        # Price / FVE
        try:
            self.price_to_FVE = to_ratio_string(to_number(self.price) / to_number(self.morningstar_FVE))
        except Exception as e:
            self.price_to_FVE = None

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

        # This is capped at +10% of current EBIT margin
        try:
            self.adj_ebit_margin = to_percent_string(min(to_number(self.ebit_margin) + 0.10, to_number(self.max_ebit_margin)))
            if self.ebit_margin is not None:
                self.adj_ebit_margin = to_percent_string((to_number(self.adj_ebit_margin) + to_number(self.ebit_margin)) / 2)
        except Exception as e:
            self.adj_ebit_margin = self.ebit_margin

        # Adjusted EBIT: max op margin 3y * current revenue
        try:
            self.adj_ebit = to_billions_string(to_number(self.adj_ebit_margin) * to_number(self.revenue))
        except Exception as e:
            self.adj_ebit = None

        # Net Income
        try:
            self.net_income = to_billions_string(to_number(self.net_margin) * to_number(self.revenue))
        except Exception as e:
            self.net_income = None

        # Enterprise value
        # If company has more cash than market cap, set EV to traditional market cap
        try:
            if to_number(self.cash) < to_number(self.market_cap):
                self.enterprise_value = to_billions_string(to_number(self.market_cap) + to_number(self.long_term_debt) - to_number(self.cash))
            else:
                self.enterprise_value = self.market_cap
        except Exception as e:
            self.enterprise_value = self.market_cap

        # EBITDA Margin
        try:
            self.ebitda_margin = to_percent_string(to_number(self.ebitda) / to_number(self.revenue))
        except Exception as e:
            self.ebitda_margin = None

        # EV to Sales Ratio
        try:
            if to_number(self.revenue) > 0:
                self.ev_to_sales_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.revenue))
            else:
                self.ev_to_sales_ratio = None
        except Exception as e:
            self.ev_to_sales_ratio = None

        # EV to Gross Profit Ratio
        try:
            if to_number(self.gross_profit) > 0:
                self.ev_to_gp_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.gross_profit))
            else:
                self.ev_to_gp_ratio = None
        except Exception as e:
            self.ev_to_gp_ratio = None

        # EV to EBITDA Ratio
        try:
            self.ev_to_ebitda_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.ebitda))
        except Exception as e:
            self.ev_to_ebitda_ratio = None

        # EV to EBIT Ratio
        try:
            if to_number(self.ebit):
                self.ev_to_ebit_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.ebit))
            else:
                self.ev_to_ebit_ratio = None
        except Exception as e:
            self.ev_to_ebit_ratio = None

        # Adjusted EV to EBIT Ratio
        try:
            if to_number(self.adj_ebit) > 0:
                self.adj_ev_to_ebit_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.adj_ebit))
            else:
                self.adj_ev_to_ebit_ratio = None
        except Exception as e:
            self.adj_ev_to_ebit_ratio = self.ev_to_ebit_ratio

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
