import requests
import re
import ast
from utilities import *


def get_macrotrends_metrics(ticker, metric_name, *args):

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

    elif metric_name == 'Sales Y/Y':
        try:
            # This URL is from a specific chart on the Macrotrends revenue page
            url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=revenue&statement=income-statement&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)

            revenue_current = chartData[-1]['v1']
            revenue_last = chartData[-5]['v1']
            revenue_growth = to_percent_string((revenue_current / revenue_last) - 1)

            return revenue_growth
        except Exception as e:
            return None

    elif metric_name == 'EBITDA':
        # This URL is from a specific chart on the Macrotrends revenue page

        url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=ebitda&statement=income-statement&freq=Q' % ticker
        html_doc = requests.get(url).text

        # Search the html_doc using regex for the chart content and set to chartData variable.
        result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
        result = result.replace('null', '"NULL"')
        chartData = ast.literal_eval(result)

        return to_billions_string(chartData[-1]['v1'] * 1000000000)

    elif metric_name == 'EBITDA past 3Y':
        try:
            # This URL is from a specific chart on the Macrotrends revenue page

            url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=ebitda&statement=income-statement&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)

            return to_percent_string((chartData[-1]['v1'] / chartData[-13]['v1']) ** (1/3) - 1)
        except Exception as e:
            return None

    elif metric_name == 'Max Operating Margin 3Y':
        try:
            # This URL is from a specific chart on the Macrotrends revenue page

            url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=operating-margin&statement=ratios&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)

            return to_percent_string(max(chartData[-12:], key=lambda x: x.get('v3', -1))['v3'] / 100)
        except Exception as e:
            return None

    elif metric_name == 'Median Rev Growth 3Y':
        try:
            # This URL is from a specific chart on the Macrotrends revenue page

            url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=revenue&statement=income-statement&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)
            chartData = [x for x in chartData if x.get('v3', 'NULL') != 'NULL']  # Remove list items with 'v3' items == 'NULL'
            if len(chartData) >= 12 and chartData[-12]['v3'] != 'NULL':
                sorted_list = sorted(chartData[-12:], key=lambda x: x.get('v3', chartData[-1]['v3']))
            else:
                sorted_list = sorted(chartData, key=lambda x: x.get('v3', chartData[-1]['v3']))

            return to_percent_string(sorted_list[len(sorted_list) // 2]['v3'] / 100)
        except Exception as e:
            return None

    elif metric_name == '% Change in Share Count 3Y':
        try:
            # This URL is from a specific chart on the Macrotrends revenue page

            url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=shares-outstanding&statement=income-statement&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)
            chartData = [x for x in chartData if x.get('v2', 'NULL') != 'NULL'][-13:]  # Remove list items with 'v3' items == 'NULL'
            if len(chartData) == 13:
                return to_percent_string((chartData[-1]['v2'] / chartData[0]['v2']) ** (1.0/3) - 1)
        except Exception as e:
            return None

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

        except Exception as e:
            return 0

    elif metric_name == 'Research and Development':
        try:
            # This URL is from a specific chart on the Macrotrends revenue page
            url = 'http://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=research-development-expenses&statement=income-statement&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)
            chartData = [x for x in chartData if x.get('v1', 'NULL') != 'NULL']

            return to_billions_string(to_number(chartData[-1]['v1']) * 1000000000)

        except Exception as e:
            return None
