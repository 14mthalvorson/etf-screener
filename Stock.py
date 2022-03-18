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

        finviz_fundamentals = get_finviz_metrics(ticker, ['Company', 'Price', 'Market Cap', 'Sector', 'Industry', 'Sales', 'Dividend %', 'P/E', 'P/S',
                                                 'EPS this Y', 'Sales Q/Q', 'Sales past 5Y', 'Gross Margin',
                                                 'Oper. Margin', 'Profit Margin', 'Beta', 'SMA20', 'SMA50', 'SMA200', '52W High', '52W Low',
                                                 'Perf Year', 'Shs Outstand', 'P/C', 'P/FCF', 'Debt/Eq', 'Employees', 'Volatility M', 'Volatility W', 'Country'])

        if finviz_fundamentals['Market Cap'] is None:  # Probably an ETF
            self.type = 'ETF'

        # Basic Data Collection
        self.name = finviz_fundamentals['Company']
        self.price = finviz_fundamentals['Price']
        self.market_cap = finviz_fundamentals['Market Cap']
        self.shares = finviz_fundamentals['Shs Outstand']
        self.sector = finviz_fundamentals['Sector']
        self.industry = finviz_fundamentals['Industry']
        self.country = finviz_fundamentals['Country']

        self.three_year_return, self.five_year_return, self.ten_year_return = get_macrotrends_metrics(ticker, 'Stock Prices')

        self.revenue = finviz_fundamentals['Sales']
        self.ebitda = get_macrotrends_metrics(ticker, 'EBITDA')

        self.pe_ratio = finviz_fundamentals['P/E']
        self.ps_ratio = finviz_fundamentals['P/S']

        self.qoq_rev_growth = finviz_fundamentals['Sales Q/Q']
        self.ttm_rev_growth, self.med_ttm_rev_growth_3y, self.med_qoq_rev_growth_3y, self.annualized_rev_growth_3y, self.med_qoq_rev_growth_5y = get_macrotrends_metrics(ticker, 'Rev Growth')
        self.annualized_rev_growth_5y = finviz_fundamentals['Sales past 5Y']

        self.gp_growth_3y, self.gp_growth_5y, self.gp_growth_10y = get_macrotrends_metrics(ticker, 'GP Growth')

        self.gross_margin, self.ebit_margin, self.net_margin, self.max_ebit_margin = get_macrotrends_metrics(ticker, 'Margins')

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
        self.monthly_volatility = finviz_fundamentals['Volatility M']
        self.weekly_volatility = finviz_fundamentals['Volatility W']

        self.morningstar_FVE = morningstar_FVEs.get(ticker, None)

        # Value checks
        if self.revenue == '-':
            self.revenue = None

        if self.med_ttm_rev_growth_3y is not None and to_number(self.med_ttm_rev_growth_3y) < -0.25:
            self.med_ttm_rev_growth_3y = None

        if self.gross_margin is None:
            self.gross_margin = finviz_fundamentals['Gross Margin']
        if self.ebit_margin is None:
            self.ebit_margin = finviz_fundamentals['Oper. Margin']
        if self.net_margin is None:
            self.net_margin = finviz_fundamentals['Profit Margin']

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
            if to_number(self.adj_rev_growth_3y) > 2.00 or to_number(self.adj_rev_growth_3y) < -0.20 or len(revs) <= 2:  # Cap max growth to 200%, min growth to -20%. Also must have values for at least 3 rev metrics.
                self.adj_rev_growth_3y = None
        except Exception as e:
            self.adj_rev_growth_3y = self.annualized_rev_growth_3y

        self.leveraged_adj_rev_growth_3y = self.adj_rev_growth_3y

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

        try:
            if self.max_ebit_margin is not None:
                self.adj_ebit_margin = self.max_ebit_margin
            else:
                self.adj_ebit_margin = self.ebit_margin
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
            if to_number(self.ebit) and to_number(self.ebit_margin) > 0.02:
                self.ev_to_ebit_ratio = to_ratio_string(to_number(self.enterprise_value) / to_number(self.ebit))
            else:
                self.ev_to_ebit_ratio = None
        except Exception as e:
            self.ev_to_ebit_ratio = None

        # Adjusted EV to EBIT Ratio
        try:
            if to_number(self.adj_ebit_margin) > 0.02:
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

        # Generate "Martin" Score - my arbitrary scoring system for finding ETFs I like
        martin_score = 0

        # Revenue growth > 8%
        try:
            if to_number(self.adj_rev_growth_3y) >= 0.08:
                martin_score += 1
        except Exception as e:
            pass

        # Revenue growth > 15%
        try:
            if to_number(self.adj_rev_growth_3y) >= 0.15:
                martin_score += 1
        except Exception as e:
            pass

        # Revenue growth > 25%
        try:
            if to_number(self.adj_rev_growth_3y) >= 0.25:
                martin_score += 1
        except Exception as e:
            pass

        # Revenue growth > 40%
        try:
            if to_number(self.adj_rev_growth_3y) >= 0.40:
                martin_score += 1
        except Exception as e:
            pass

        try:
            if to_number(self.ev_to_gp_ratio) <= 15.0:
                martin_score += 1
        except Exception as e:
            pass

        try:
            if to_number(self.adj_ev_to_ebit_ratio) <= 30.0:
                martin_score += 1
        except Exception as e:
            pass

        try:
            if to_number(self.adj_ebit_margin) >= 0.00:
                martin_score += 1
        except Exception as e:
            pass

        try:
            if to_number(self.adj_ebit_margin) >= 0.20:
                martin_score += 1
        except Exception as e:
            pass

        try:
            if to_number(self.gross_margin) >= 0.60:
                martin_score += 1
        except Exception as e:
            pass

        try:
            if to_number(self.monthly_volatility) <= 0.04:
                martin_score += 1
        except Exception as e:
            pass

        self.martin_score = str(martin_score)
        if self.num_holdings == '0':
            self.martin_score = None
