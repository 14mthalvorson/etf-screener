from datetime import date

import requests
import re
import ast
from utilities import *


def get_macrotrends_metrics(ticker, metric_name, *args):

    if metric_name == 'EBITDA past 3Y':
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

    # Returns gross, operating, profit margins
    elif metric_name == 'Margins':
        try:
            url = 'https://www.macrotrends.net/assets/php/fundamental_metric.php?t=%s&chart=profit-margin' % ticker
            html_doc = requests.get(url).text

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)
            try:
                gross_margin = str(chartData[-1]['v1']) + '%'
            except Exception as e:
                gross_margin = None
            try:
                ebit_margin = str(chartData[-1]['v2']) + '%'
            except Exception as e:
                ebit_margin = None
            try:
                net_margin = str(chartData[-1]['v3']) + '%'
            except Exception as e:
                net_margin = None
            try:
                max_ebit_margin_2y = to_percent_string(max(chartData[-8:], key=lambda x: x.get('v2', -1))['v2'] / 100)
            except Exception as e:
                max_ebit_margin_2y = None

            return gross_margin, ebit_margin, net_margin, max_ebit_margin_2y
        except Exception as e:
            return None, None, None, None

    # Returns 3, 5, 10 year stock performances if available
    elif metric_name == 'Stock Prices':
        try:
            today_str = [int(x) for x in str(date.today()).split('-')]

            url = 'https://www.macrotrends.net/assets/php/stock_price_history.php?t=%s' % ticker
            html_doc = requests.get(url).text
            result = re.search('var dataDaily = \[.*]', html_doc).group(0)[16:]
            chartData = ast.literal_eval(result)
            now = to_number([day.get('c', -1) for day in chartData if str(date.today())[:8] in day.get('d', '')][0])

            try:
                if today_str[1] < 10:
                    three_past = str(today_str[0] - 3) + '-0' + str(today_str[1])
                else:
                    three_past = str(today_str[0] - 3) + '-' + str(today_str[1])
                old = to_number([day.get('c', -1) for day in chartData if three_past in day.get('d', '')][0])
                three = to_percent_string((now / old) ** (1/3) - 1)

            except Exception as e:
                three = None
            try:
                if today_str[1] < 10:
                    five_past = str(today_str[0] - 5) + '-0' + str(today_str[1])
                else:
                    five_past = str(today_str[0] - 5) + '-' + str(today_str[1])
                old = to_number([day.get('c', -1) for day in chartData if five_past in day.get('d', '')][0])
                five = to_percent_string((now / old) ** (1/5) - 1)

            except Exception as e:
                five = None
            try:
                if today_str[1] < 10:
                    ten_past = str(today_str[0] - 10) + '-0' + str(today_str[1])
                else:
                    ten_past = str(today_str[0] - 10) + '-' + str(today_str[1])
                old = to_number([day.get('c', -1) for day in chartData if ten_past in day.get('d', '')][0])
                ten = to_percent_string((now / old) ** (1/10) - 1)

            except Exception as e:
                ten = None

            return three, five, ten
        except Exception as e:
            return None, None, None

    elif metric_name == 'Rev Growth':
        try:
            url = 'https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=%s&type=revenue&statement=income-statement&freq=Q' % ticker
            html_doc = requests.get(url).text
            result = re.search('var chartData = \[.*]', html_doc).group(0)[16:]
            result = result.replace('null', '"NULL"')
            chartData = ast.literal_eval(result)

            temp = [x for x in chartData if x.get('v1', 'NULL') != 'NULL']  # Remove list items with 'v1' items == 'NULL'
            ttm_rev_growth = to_percent_string(to_number(temp[-1]['v1']) / to_number(temp[-5]['v1']) - 1)
        except Exception as e:
            ttm_rev_growth = None

        try:
            temp = [x for x in chartData if x.get('v1', 'NULL') != 'NULL']  # Remove list items with 'v1' items == 'NULL'
            temp = temp[-17:]
            res = []
            for i, point in enumerate(temp):
                if i >= 4:
                    try:
                        res.append(to_percent_string(to_number(temp[i]['v1']) / to_number(temp[i - 4]['v1']) - 1))
                    except Exception as e:
                        pass
            res.sort(key=lambda x: to_number(x))
            answer = res[len(res) // 2]
            med_ttm_rev_growth_3y = answer
        except Exception as e:
            med_ttm_rev_growth_3y = None

        try:
            med_qoq_rev_growth_3y = 0
            temp = [x for x in chartData if x.get('v3', 'NULL') != 'NULL']  # Remove list items with 'v3' items == 'NULL'
            if len(temp) >= 12 and temp[-12]['v3'] != 'NULL':  # Ideally take last 12 quarters of history
                sorted_list = sorted(temp[-12:], key=lambda x: x.get('v3', temp[-1]['v3']))
            elif len(temp) >= 3 and temp[-3]['v3'] != 'NULL':  # At minimum, require 3 quarters of history
                sorted_list = sorted(temp, key=lambda x: x.get('v3', temp[-1]['v3']))
            else:
                med_qoq_rev_growth_3y = None
            if med_qoq_rev_growth_3y is not None:
                med_qoq_rev_growth_3y = to_percent_string(sorted_list[len(sorted_list) // 2]['v3'] / 100)
        except Exception as e:
            med_qoq_rev_growth_3y = None

        try:
            temp = [x for x in chartData]
            while len(temp) > 0 and temp[-1].get('v1', 'NULL') == 'NULL':
                temp.pop(-1)
            temp = temp[-13:]
            while len(temp) > 0 and temp[0].get('v1', 'NULL') == 'NULL':
                temp.pop(0)
            annualized_rev_growth_3y = to_percent_string((to_number(temp[-1]['v1']) / to_number(temp[0]['v1'])) ** (4.0 / (len(temp) - 1)) - 1)
        except Exception as e:
            annualized_rev_growth_3y = None

        try:
            temp = [x for x in chartData if x.get('v3', 'NULL') != 'NULL']  # Remove list items with 'v3' items == 'NULL'
            sorted_list = sorted(temp[-20:], key=lambda x: x.get('v3', temp[-1]['v3']))
            med_qoq_rev_growth_5y = to_percent_string(sorted_list[len(sorted_list) // 2]['v3'] / 100)
        except Exception as e:
            med_qoq_rev_growth_5y = None

        try:
            return ttm_rev_growth, med_ttm_rev_growth_3y, med_qoq_rev_growth_3y, annualized_rev_growth_3y, med_qoq_rev_growth_5y
        except Exception as e:
            return None, None, None, None, None

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
