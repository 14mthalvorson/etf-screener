# Finviz Finance - one of the sources of financial information
# Uses the finvizfinance Python library to access financial information

"""
Example metrics to search for
{
'Company': 'Amazon.com, Inc.',
'Sector': 'Consumer Cyclical',
'Industry': 'Internet Retail',
'Country': 'USA',
'Index': 'S&P 500',
'P/E': '66.28',
'EPS (ttm)': '51.14',
'Insider Own': '9.90%',
'Shs Outstand': '507.00M',
'Perf Week': '-3.27%',
'Market Cap': '1743.23B',
'Forward P/E': '65.54',
'EPS next Y': '26.34%',
'Insider Trans': '-1.97%',
'Shs Float': '439.25M',
'Perf Month': '0.17%',
'Income': '26.26B',
'PEG': '1.84',
'EPS next Q': '21.43',
'Inst Own': '59.30%',
'Short Float': '0.96%',
'Perf Quarter': '-2.54%',
'Sales': '457.96B',
'P/S': '3.81',
'EPS this Y': '81.90%',
'Inst Trans': '-0.52%',
'Short Ratio': '1.32',
'Perf Half Y': '6.00%',
'Book/sh': '237.80',
'P/B': '14.25',
'ROA': '7.60%',
'Target Price': '4107.20',
'Perf Year': '6.37%',
'Cash/sh': '153.60',
'P/C': '22.07',
'EPS next 5Y': '36.00%',
'ROE': '24.30%',
'52W Range From': '2881.00',
'52W Range To': '3773.08',
'Perf YTD': '4.08%',
'Dividend': '-',
'P/FCF': '-',
'EPS past 5Y': '101.80%',
'ROI': '13.90%',
'52W High': '-10.16%',
'Beta': '1.13',
'Dividend %': '-',
'Quick Ratio': '0.90',
'Sales past 5Y': '29.30%',
'Gross Margin': '41.30%',
'52W Low': '17.66%',
'ATR': '98.89',
'Employees': '1335000',
'Current Ratio': '1.10',
'Sales Q/Q': '15.30%',
'Oper. Margin': '6.20%',
'RSI (14)': '41.78',
'Volatility W': '2.78%',
'Volatility M': '2.77%',
'Optionable': 'Yes',
'Debt/Eq': '0.55',
'EPS Q/Q': '-50.40%',
'Profit Margin': '5.70%',
'Rel Volume': '1.23',
'Prev Close': '3437.36',
'Shortable': 'Yes',
'LT Debt/Eq': '0.55',
'Earnings': 'Oct 28 AMC',
'Payout': '0.00%',
'Avg Volume': '3.21M',
'Price': '3389.79',
'Recom': '1.70',
'SMA20': '-4.16%',
'SMA50': '-0.84%',
'SMA200': '1.12%',
'Volume': '3,955,629',
'Change': '-1.38%'
}
"""

from finvizfinance.quote import finvizfinance


# Single value - Takes a ticker and a single desired metrics and returns the value of the desired metric
# Multiple values - Takes a ticker and a list of desired metric names and returns a dictionary of the desired metrics
def get_finviz_metrics(ticker, metric_names):
    stock = finvizfinance(ticker)
    fundamentals = stock.TickerFundament()

    if isinstance(metric_names, list):
        metrics = {}

        for metric_name in metric_names:
            try:
                metrics[metric_name] = fundamentals[metric_name]
            except Exception as e:
                print(e)

        return metrics

    else:
        try:
            return fundamentals[metric_names]
        except Exception as e:
            print(e)
