import yfinance
from finviz_finance_fulfillment import get_finviz_metrics
from utilities import *


# Takes a ticker and a list of desired metric names and returns a dictionary of the desired metrics
def get_yfinance_metrics(ticker, list_of_metric_names):
    metrics = {}
    stock = yfinance.Ticker(ticker)

    # For 'Sales past 3Y' calculation is actually a weighted average of past year and last 2 complete years
    # TODO: Fix this 'Sales past 3Y' function
    if 'Sales past 3Y' in list_of_metric_names:
        try:
            old_revenues = stock.earnings.values
            prior_revenue_growth = 1.0 * old_revenues[3,0] / old_revenues[1,0]
            last_year_revenue = to_number(get_finviz_metrics(ticker, 'Sales Q/Q')) + 1
            metrics['Sales past 3Y'] = to_percent_string((last_year_revenue * prior_revenue_growth) ** (1.0/3) - 1)
        except Exception as e:
            print(e)

    return metrics
