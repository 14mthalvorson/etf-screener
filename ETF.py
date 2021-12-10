import requests
import re
from Stock import *


class ETF:

    def __init__(self, ticker):
        self.ticker = ticker
        self.holdings = self.fill_holdings_from_marketwatch()
        self.weighted_revenue_growth = self.calculate_weighted_revenue_growth()
        self.weighted_revenue_growth_3y = self.calculate_weighted_revenue_growth_3y()
        self.weighted_EV_to_EBITDA_ratio = self.calculate_weighted_EV_to_EBITDA_ratio()

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

    def calculate_weighted_revenue_growth_3y(self):
        weighted_numer = 0
        weighted_denom = 0

        for ticker in self.holdings.keys():
            try:
                stock = Stock(ticker)

                # Ignore outliers above 100% 3Y revenue growth
                if stock.revenue_growth_3y is not None and to_number(stock.revenue_growth_3y) < 1.00:
                    weighted_numer += to_number(stock.revenue_growth_3y) * to_number(self.holdings[ticker])
                    weighted_denom += to_number(self.holdings[ticker])

            except OverflowError:
                pass

            except Exception as e:
                # Some companies don't have this. That is fine. Don't really need to notify.
                pass

        if weighted_denom != 0:
            return to_percent_string(weighted_numer / weighted_denom)
        else:
            return None

    # EV/EBITDA Ratio
    # 1. Sum all weighted EBITDA. 2. Sum all weighted EV. 3. Calculate the ratio.
    def calculate_weighted_EV_to_EBITDA_ratio(self):
        weighted_EV = 0
        weighted_EBITDA = 0

        for ticker in self.holdings.keys():
            try:
                stock = Stock(ticker)

                if stock.ebitda is not None:
                    weighted_EBITDA += to_number(stock.ebitda)
                    weighted_EV += to_number(stock.enterprise_value)

            except OverflowError:
                pass

            except Exception as e:
                pass
                #print('passing on:', ticker, "(weighted EV/EBITDA)", e)

        if weighted_EBITDA != 0:
            return to_ratio_string(weighted_EV / weighted_EBITDA)
        else:
            return 'None'

    def display_holdings_metric(self):
        for ticker in self.holdings.keys():
            try:
                stock = Stock(ticker)

                if stock.revenue_growth_3y is not None and stock.ev_to_ebitda_ratio and to_number(stock.ev_to_ebitda_ratio) > 0:
                    print(stock.ticker + '\t' + stock.revenue_growth_3y + '\t' + stock.ev_to_ebitda_ratio)

            except OverflowError:
                pass

            except Exception as e:
                pass
                # print('passing on:', ticker, "(weighted EV/EBITDA)", e)
