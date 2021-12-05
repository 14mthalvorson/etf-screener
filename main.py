from Stock import *


aapl = Stock('aapl')

# Tickers are now callable as ticker objects

print(aapl.company)
print('Cash', aapl.cash)
print('FCF', aapl.free_cash_flow)
