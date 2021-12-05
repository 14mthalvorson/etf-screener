from Stock import *


aapl = Stock('aapl')

# Tickers are now callable as ticker objects
for variable in [aapl]:
    print(variable.company)
    print('Sales past 3Y', variable.revenue_growth_3y)
    print('')
