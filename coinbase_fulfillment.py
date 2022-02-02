import requests
import re
import ast
from utilities import *


def get_coinbase_data(ticker, metric_name):

    if metric_name == 'Sales past 3Y':
        try:
            # This URL is from a specific chart on the Macrotrends revenue page
            url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=revenue&statement=income-statement&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)

            revenue_current = chartData[-1]['v1']
            revenue_3Y = chartData[-13]['v1']
            annualized_revenue_3Y = to_percent_string((revenue_current / revenue_3Y) ** (1 / 3) - 1)

            return annualized_revenue_3Y
        except Exception as e:
            return None

