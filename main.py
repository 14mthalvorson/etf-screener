from Ticker import *


amzn = Ticker('amzn')
googl = Ticker('googl')
msft = Ticker('msft')
fb = Ticker('fb')
aapl = Ticker('aapl')

# Tickers are now callable as ticker objects
for variable in [amzn, googl, msft, fb, aapl]:
    print(variable.company)
    print('Gross Income:', variable.gross_income)
    print('Operating Income:', variable.operating_income)
    print('')
