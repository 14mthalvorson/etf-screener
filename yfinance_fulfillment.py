import yfinance as yf
from finviz_finance_fulfillment import get_finviz_metrics
from utilities import *


# Takes a ticker and a list of desired metric names and returns a dictionary of the desired metrics
def get_yfinance_metrics(ticker):
    stock = yf.Ticker(ticker)
    metrics = {}
    metrics['Research & Development'] = stock.quarterly_financials.iloc[0][0] + stock.quarterly_financials.iloc[0][1] + stock.quarterly_financials.iloc[0][2] + stock.quarterly_financials.iloc[0][3]
    return metrics
