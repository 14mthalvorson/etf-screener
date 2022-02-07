import requests
import re
import ast
from utilities import *


def get_macrotrends_metrics(ticker, metric_name, *args):

    if metric_name == 'EBITDA':
        try:
            # This URL is from a specific chart on the Macrotrends revenue page

            url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=ebitda&statement=income-statement&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)

            return to_billions_string(chartData[-1]['v1'] * 1000000000)
        except Exception as e:
            return None

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

    # This is capped at +10% of current EBIT margin
    elif metric_name == 'Max EBIT Margin 3Y':
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

    elif metric_name == 'TTM Rev Growth':
        try:
            # This URL is from a specific chart on the Macrotrends revenue page

            url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=revenue&statement=income-statement&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)
            chartData = [x for x in chartData if x.get('v1', 'NULL') != 'NULL']  # Remove list items with 'v1' items == 'NULL'
            return to_percent_string(to_number(chartData[-1]['v1']) / to_number(chartData[-5]['v1']) - 1)
        except Exception as e:
            return None

    elif metric_name == 'Median TTM Rev Growth 3Y':
        '''
        This is an important metric. Used in many calculations.
        Ideally, take the annualized revenue growth rate from the last 13 quarters (will need 17 quarters of TTM revenue)

        Calculation:
        Take v1 row. Clean all the null values out. Chop down to max 20 values.
        Starting with index 4, calculate TTM (annual) revenue growth rate for as many values as possible.
        When done, take median.

        Return None if errors.
        '''
        try:
            # This URL is from a specific chart on the Macrotrends revenue page

            url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=revenue&statement=income-statement&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)
            chartData = [x for x in chartData if x.get('v1', 'NULL') != 'NULL']  # Remove list items with 'v1' items == 'NULL'
            chartData = chartData[-17:]
            res = []
            for i, point in enumerate(chartData):
                if i >= 4:
                    try:
                        res.append(to_percent_string(to_number(chartData[i]['v1']) / to_number(chartData[i - 4]['v1']) - 1))
                    except Exception as e:
                        pass
            res.sort(key=lambda x: to_number(x))
            answer = res[len(res) // 2]
            # If answer is more than 20% different than neighboring values, it has a high chance of not being a good figure to use
            '''
            if to_number(res[len(res) // 2 + 1]) - to_number(res[len(res) // 2 - 1]) > 0.2:
                return None
            '''
            return answer
        except Exception as e:
            return None

    elif metric_name == 'Median Q/Q Rev Growth 3Y':
        try:
            # This URL is from a specific chart on the Macrotrends revenue page

            url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=revenue&statement=income-statement&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)
            chartData = [x for x in chartData if x.get('v3', 'NULL') != 'NULL']  # Remove list items with 'v3' items == 'NULL'
            if len(chartData) >= 12 and chartData[-12]['v3'] != 'NULL':  # Ideally take last 12 quarters of history
                sorted_list = sorted(chartData[-12:], key=lambda x: x.get('v3', chartData[-1]['v3']))
            elif len(chartData) >= 3 and chartData[-3]['v3'] != 'NULL':  # At minimum, require 3 quarters of history
                sorted_list = sorted(chartData, key=lambda x: x.get('v3', chartData[-1]['v3']))
            else:
                return None

            return to_percent_string(sorted_list[len(sorted_list) // 2]['v3'] / 100)
        except Exception as e:
            return None

    elif metric_name == 'Annualized Rev Growth 3Y':
        '''
        Doesn't remove null quarters because that would mess up the length of time
        Just makes sure the ends are valid.
        '''
        try:
            # This URL is from a specific chart on the Macrotrends revenue page

            url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=revenue&statement=income-statement&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)
            while len(chartData) > 0 and chartData[-1].get('v1', 'NULL') == 'NULL':
                chartData.pop(-1)
            chartData = chartData[-13:]
            while len(chartData) > 0 and chartData[0].get('v1', 'NULL') == 'NULL':
                chartData.pop(0)

            return to_percent_string((to_number(chartData[-1]['v1']) / to_number(chartData[0]['v1'])) ** (4.0 / (len(chartData) - 1)) - 1)

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

            url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=long-term-debt&statement=balance-sheet&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)
            chartData = [x for x in chartData if x.get('v2', 'NULL') != 'NULL']

            return to_billions_string(to_number(chartData[-1]['v2']) * 1000000000)

        except Exception as e:
            return 0

    elif metric_name == 'Cash':
        try:
            # This URL is from a specific chart on the Macrotrends revenue page
            url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=cash-on-hand&statement=balance-sheet&freq=Q' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)
            chartData = [x for x in chartData if x.get('v2', 'NULL') != 'NULL']

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
