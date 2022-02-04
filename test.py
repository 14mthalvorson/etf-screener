# Very basic troubleshooting test file for the common functions
from ETF import *
from Stock import *


try:
    aapl = Stock('aapl')
    print('AAPL price: ', aapl.price)
except Exception as e:
    print(1, 'Error with Finviz and getting stock price.')
    print(e)

try:
    msft = Stock('msft')
    print('MSFT revenue growth Y/Y: ', msft.revenue_growth_yoy)
except Exception as e:
    print(2, 'Error with Macrotrends and retrieving revenue growth.')

try:
    etf = ETF('vig')
    print('VIG weights: ', etf.weights)
except Exception as e:
    print(3, 'Error with Marketwatch and getting ETF holdings.')
    print(e)

print('Done with tests.')
