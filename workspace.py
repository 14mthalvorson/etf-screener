from ETF import *
from utilities import *
import ast
import pickle
from datetime import date

ticker = 'amzn'

today_str = [int(x) for x in str(date.today()).split('-')]
if today_str[1] < 10:
    five_past = str(today_str[0] - 5) + '-0' + str(today_str[1])
else:
    five_past = str(today_str[0] - 5) + '-' + str(today_str[1])

print(five_past)

url = 'https://www.macrotrends.net/assets/php/stock_price_history.php?t=%s' % ticker
html_doc = requests.get(url).text

# Search the html_doc using regex for the chart content and set to chartData variable.
result = re.search('var dataDaily = \[.*]', html_doc).group(0)[16:]
chartData = ast.literal_eval(result)

old = to_number([day.get('c', -1) for day in chartData if five_past in day.get('d', '')][0])
now = to_number([day.get('c', -1) for day in chartData if str(date.today())[:8] in day.get('d', '')][0])

print(old)
print(now)
print(to_percent_string((now / old) ** (1/5) - 1))

# print(chartData)

exit(0)

'''
stock = finvizfinance('qqq')
fundamentals = stock.ticker_fundament()
print(fundamentals)

# clean_tickers_to_dict()

stock = yf.Ticker('aapl')
print(stock.quarterly_financials.iloc[0][0])
print(stock.quarterly_cashflow)
print(stock.quarterly_balance_sheet)
print(stock.quarterly_balance_sheet.iloc[20][0])
'''

# income statement
# EBIT

# from balance sheet:
# total debt
# total cash
# net tangible assets

# from cash flow:
# capex
# free cash flow
# share buybacks

# Can also get crypto data from Yahoo Finance
# fiftyTwoWeekHigh
# 52W High Drawdown (calculate)

# Key Statistics
# beta (5Y monthly)
# morningStarOverallRating
# pegRatio
# enterpriseValue

'''
Yahoo Finance Modules
get interest expense
get total revenue
get research and development
get ebit()



# calculation debt/operating profit

yf = YahooFinancials(['aapl', 'googl', 'msft', 'fb', 'amzn'])
#bsh = list(yf.get_financial_stmts('annual', 'balance')['balanceSheetHistory']['AAPL'][0].values())[0]
#print(bsh['cash'])
#ish = list(yf.get_financial_stmts('annual', 'income')['incomeStatementHistory']['AAPL'][0].values())[0]
#print(ish['ebit'])
# very rate limited API

print(yf.get_ebit())
print(yf.get_beta())
print(yf.get_research_and_development())
'''
