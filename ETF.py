import requests
import re
from Stock import *


class ETF:

    def __init__(self, ticker):
        self.ticker = ticker
        self.holdings = self.fill_holdings_from_marketwatch()

        # Hardcode ETF weightings here
        # self.holdings = {'amzn':'10.00%', 'aapl':'10.00%', 'googl':'10.00%', 'fb':'10.00%', 'nflx':'10.00%', 'nvda':'10.00%', 'tsla':'10.00%', 'twtr':'10.00%', 'bidu':'10.00%', 'baba':'10.00%'}
        self.holdings = {'amzn': '1.00%', 'aapl': '1.00%', 'msft': '1.00%', 'googl': '1.00%', 'goog': '1.00%', 'fb': '1.00%', 'tsm': '1.00%', 'tsla': '1.00%', 'nvda': '1.00%', 'v': '1.00%',
                         'ma': '1.00%', 'adbe': '1.00%', 'dis': '1.00%', 'nflx': '1.00%', 'crm': '1.00%', 'pypl': '1.00%', 'shop': '1.00%', 'se': '1.00%', 'now': '1.00%', 'snow': '1.00%',
                         'abnb': '1.00%', 'team': '1.00%', 'sq': '1.00%', 'snap': '1.00%', 'wday': '1.00%', 'coin': '1.00%', 'zm': '1.00%', 'ddog': '1.00%', 'twlo': '1.00%', 'ttd': '1.00%',
                         'crwd': '1.00%', 'net': '1.00%', 'zs': '1.00%', 'veev': '1.00%', 'u': '1.00%', 'pltr': '1.00%', 'twtr': '1.00%', 'hubs': '1.00%', 'okta': '1.00%', 'etsy': '1.00%',
                         'bill': '1.00%', 'pins': '1.00%', 'tyl': '1.00%', 'hood': '1.00%', 'rng': '1.00%', 'zen': '1.00%', 'coup': '1.00%', 'open': '1.00%', 'appf': '1.00%', 'amd': '1.00%',
                         'mu': '1.00%', 'intc': '1.00%', 'intu': '1.00%', 'isrg': '1.00%', 'cost': '1.00%', 'wmt': '1.00%', 'tgt': '1.00%', 'qcom': '1.00%', 'avgo': '1.00%', 'cmcsa': '1.00%',
                         'prp': '1.00%', 'txn': '1.00%', 'hon': '1.00%', 'amat': '1.00%', 'lrcx': '1.00%', 'adi': '1.00%', 'orcl': '1.00%', 'ibm': '1.00%', 'adsk': '1.00%', 'hd': '1.00%',
                         'xom': '1.00%', 'mrna': '1.00%', 'pfe': '1.00%', 'jnj': '1.00%', 'pg': '1.00%', 'unh': '1.00%', 'roku': '1.00%', 'brk.b': '1.00%', 'jpm': '1.00%', 'bac': '1.00%',
                         'nke': '1.00%', 'tmo': '1.00%', 'csco': '1.00%', 'ko': '1.00%', 'acn': '1.00%', 'abt': '1.00%', 'cvx': '1.00%', 'vz': '1.00%', 't': '1.00%', 'tmus': '1.00%',
                         'wfc': '1.00%', 'mcd': '1.00%', 'dpz': '1.00%', 'ups': '1.00%', 'mrk': '1.00%', 'low': '1.00%', 'ms': '1.00%', 'gs': '1.00%', 'mdt': '1.00%', 'pm': '1.00%', }

        self.weighted_revenue_growth = self.calculate_weighted_revenue_growth()
        self.weighted_revenue_growth_3y = None
        self.weighted_EV_to_EBITDA_ratio = None
        self.calculate_weighted_growth_and_valuation_metrics()

    def fill_holdings_from_marketwatch(self):

        # Retrieve URL from dictionary
        url = 'https://www.marketwatch.com/investing/fund/%s/holdings' % self.ticker

        # Get HTML from URL
        html_doc = requests.get(url).text

        # Regex for pulling tickers
        ticker_results = re.findall('(?<=<td class="table__cell u-semi">)([A-Z]+)(?=<\/td>)', html_doc)

        # Regex for pulling the weightings
        weightings_results = re.findall('(?<=<td class="table__cell">)([0-9]{1,3}.[0-9]{2}%)(?=<\/td>)', html_doc)

        # Get to use dictionary comprehension!!!
        weighted_holdings = {ticker_results[i]: weightings_results[i] for i in range(len(ticker_results))}

        return weighted_holdings

    def calculate_weighted_ev_ebitda_ratio(self):
        pass

    def calculate_weighted_revenue_growth(self):
        weighted_numer = 0
        weighted_denom = 0

        for ticker in self.holdings.keys():
            try:
                stock = Stock(ticker)

                if stock.revenue_growth_yoy is not None:
                    weighted_numer += to_number(stock.revenue_growth_yoy) * to_number(self.holdings[ticker])
                    weighted_denom += to_number(self.holdings[ticker])

            except OverflowError:
                pass

            except Exception as e:
                #print('passing on:', ticker, "(weighted revenue growth)", e)
                pass

        if weighted_denom != 0:
            return to_percent_string(weighted_numer / weighted_denom)
        else:
            return None

    def calculate_weighted_growth_and_valuation_metrics(self):
        weighted_ev_to_ebitda = 0
        weighted_revenue_growth_3y = 0
        weighted_denom = 0

        for ticker in self.holdings.keys():
            try:
                stock = Stock(ticker)

                # Ignore outliers above 100% 3Y revenue growth
                if stock.revenue_growth_3y is not None and to_number(stock.revenue_growth_3y) < 1.00 and stock.ev_to_ebitda_ratio is not None and to_number(stock.ev_to_ebitda_ratio) > 0:
                    weighted_revenue_growth_3y += to_number(stock.revenue_growth_3y) * to_number(self.holdings[ticker])
                    weighted_ev_to_ebitda += to_number(stock.ev_to_ebitda_ratio) * to_number(self.holdings[ticker])
                    weighted_denom += to_number(self.holdings[ticker])

            except OverflowError:
                pass

            except Exception as e:
                # Some companies don't have this. That is fine. Don't really need to notify.
                pass

        if weighted_denom != 0:
            self.weighted_revenue_growth_3y = to_percent_string(weighted_revenue_growth_3y / weighted_denom)
            self.weighted_EV_to_EBITDA_ratio = to_ratio_string(weighted_ev_to_ebitda / weighted_denom)
            return
        else:
            self.weighted_revenue_growth_3y = None
            self.weighted_EV_to_EBITDA_ratio = None
            return

    def display_hardcoded_metrics(self):
        for ticker in self.holdings.keys():
            try:
                stock = Stock(ticker)

                """
                # Revenue growth past 3y and EV/EBITDA
                if stock.revenue_growth_3y is not None and stock.ev_to_ebitda_ratio and to_number(stock.ev_to_ebitda_ratio) > 0:
                    print(stock.ticker + '\t' + stock.revenue_growth_3y + '\t' + stock.ev_to_ebitda_ratio + '\t' + self.holdings[stock.ticker])
                """

                # Gross profit vs employees
                if stock.employees is not None and stock.gross_profit is not None and stock.gross_profit_per_employee is not None:
                    print(stock.ticker + '\t' + stock.gross_profit + '\t' + stock.employees + '\t' + stock.gross_profit_per_employee)

            except OverflowError:
                pass

            except Exception as e:
                pass
                # print('passing on:', ticker, "(weighted EV/EBITDA)", e)
