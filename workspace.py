# I use this script to test things before I move the code over to a proper function/method

import requests
import re


# Retrieve URL from dictionary
url = 'https://www.marketwatch.com/investing/fund/qqq/holdings'

# Get HTML from URL
html_doc = requests.get(url).text

# Regex for pulling tickers
ticker_results = re.findall('(?<=<td class="table__cell u-semi">)([A-Z]+)(?=<\/td>)', html_doc)

# Regex for pulling the weightings
weightings_results = re.findall('(?<=<td class="table__cell">)([0-9]{1,3}.[0-9]{2}%)(?=<\/td>)', html_doc)

# Get to use dictionary comprehension!!!
holdings = {ticker_results[i]: weightings_results[i] for i in range(len(ticker_results))}

print(holdings)
