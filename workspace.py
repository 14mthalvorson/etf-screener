from ETF import *
from utilities import *
import ast
import pickle
from datetime import date


clean_tickers()


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
