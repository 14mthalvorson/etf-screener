# Not using this for now. Coinbase sits behind cloudflare I believe. Not suppose to scrape...
import requests
import re
import ast
from utilities import *
from utilities import mappings


def get_coinbase_data(ticker, metric_name):
    try:
        name = mappings[ticker]['name'].lower()
        if metric_name == 'All Time High':
            # Coinbase URL
            url = 'https://www.coinbase.com/price/%s' % name
            html_doc = requests.get(url).text
            print(html_doc)

            # Search the html_doc using regex for the chart content and set to chartData variable.
            result = re.search('the all time high of \$([0-9\.,]+)\.', html_doc).group(0)
            result = result.replace(',', '')

            return result

    except Exception as e:
        print(e)
        return None

