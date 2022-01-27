# Very basic troubleshooting test file for the common functions
from ETF import ETF
from Stock import Stock


try:
    stock = Stock('aapl')
    print('AAPL price: ', stock.price)
except Exception as e:
    print(1, 'Error with Finviz and getting stock price.')
    print(e)

try:
    etf = ETF('qqq')
    print('QQQ weights: ', etf.weights)
except Exception as e:
    print(2, 'Error with Marketwatch and getting ETF holdings.')
    print(e)

try:
    stock = Stock('aapl')
    print('Revenue growth: ', stock.revenue_growth_yoy)
except Exception as e:
    print(3, 'Error with scraping data from Macrotrends.')
    print(e)

print('Done with tests.')
