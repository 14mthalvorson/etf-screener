import requests
import re
from Stock import *


class ETF:

    def __init__(self, ticker):
        self.ticker = ticker
        self.holdings = self.fill_holdings_from_marketwatch()
        self.weighted_revenue_growth = self.calculate_weighted_revenue_growth()
        self.weighted_revenue_growth_3y = self.calculate_weighted_revenue_growth_3y()

    # Holdings is a dictionary of weighted holdings
    def __int__(self, ticker, holdings):
        self = ETF()
        self.holdings = holdings

    def set_holdings(self, holdings):
        self.holdings = holdings

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
                weighted_numer += to_number(stock.revenue_growth_yoy) * to_number(self.holdings[ticker])
                weighted_denom += to_number(self.holdings[ticker])

            except Exception as e:
                print('passing on ', ticker, e)

        return to_percent_string(weighted_numer / weighted_denom)

    def calculate_weighted_revenue_growth_3y(self):
        weighted_numer = 0
        weighted_denom = 0

        for ticker in self.holdings.keys():
            try:
                stock = Stock(ticker)
                weighted_numer += to_number(stock.revenue_growth_3y) * to_number(self.holdings[ticker])
                weighted_denom += to_number(self.holdings[ticker])

            except Exception as e:
                print('passing on ', ticker, e)

        return to_percent_string(weighted_numer / weighted_denom)
