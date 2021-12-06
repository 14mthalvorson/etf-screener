import yfinance
from finviz_finance_fulfillment import get_finviz_metrics
from utilities import *


# Takes a ticker and a list of desired metric names and returns a dictionary of the desired metrics
def get_yfinance_metrics(ticker, list_of_metric_names):
    metrics = {}
    stock = yfinance.Ticker(ticker)

    return metrics
