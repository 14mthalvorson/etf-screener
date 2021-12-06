import requests
import re
import ast
from utilities import *

def get_macrotrends_metrics(ticker, metric_name):

    if metric_name == 'Sales past 3Y':
        # This URL is from a specific chart on the Macrotrends revenue page

        url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=revenue&statement=income-statement&freq=Q' % ticker
        html_doc = requests.get(url).text

        # Search the html_doc using regex for the chart content and set to chartData variable.
        chartData = ast.literal_eval(re.search('var chartData = \[.*]', html_doc).group(0)[16:])

        revenue_current = chartData[-1]['v1']
        revenue_3Y = chartData[-13]['v1']
        annualized_revenue_3Y = to_percent_string((revenue_current / revenue_3Y) ** (1 / 3) - 1)

        return annualized_revenue_3Y

    elif metric_name == 'Sales Y/Y':
        # This URL is from a specific chart on the Macrotrends revenue page
        url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=revenue&statement=income-statement&freq=Q' % ticker
        html_doc = requests.get(url).text

        # Search the html_doc using regex for the chart content and set to chartData variable.
        chartData = ast.literal_eval(re.search('var chartData = \[.*]', html_doc).group(0)[16:])

        revenue_current = chartData[-1]['v1']
        revenue_last = chartData[-5]['v1']
        revenue_growth = to_percent_string((revenue_current / revenue_last) ** (1 / 3) - 1)

        return revenue_growth

    elif metric_name == 'EBITDA':
        # This URL is from a specific chart on the Macrotrends revenue page

        url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=ebitda&statement=income-statement&freq=Q' % ticker
        html_doc = requests.get(url).text

        # Search the html_doc using regex for the chart content and set to chartData variable.
        chartData = ast.literal_eval(re.search('var chartData = \[.*]', html_doc).group(0)[16:])

        return to_billions_string(chartData[-1]['v1'] * 1000000000)

    elif metric_name == 'Long Term Debt':
        try:
            # This URL is from a specific chart on the Macrotrends revenue page

            url = 'http://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=long-term-debt&statement=balance-sheet&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)

            return to_billions_string(to_number(chartData[-1]['v2']) * 1000000000)

        except:
            return 0