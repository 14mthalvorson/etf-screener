from Stock import *


aapl = Stock('aapl')
amzn = Stock('amzn')
fb = Stock('fb')
googl = Stock('googl')
msft = Stock('msft')


# Tickers are now callable as ticker objects
variables = [aapl, amzn, fb, googl, msft]
for variable in variables:
    print(variable.company)
    print('EV/EBITDA:', variable.ev_to_ebitda_ratio)
    print()
