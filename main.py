from Stock import *


v = Stock('v')
ma = Stock('ma')
dis = Stock('dis')
nflx = Stock('nflx')
pypl = Stock('pypl')


# Tickers are now callable as ticker objects
variables = [v, ma, dis, nflx, pypl]
for variable in variables:
    print(variable.company)
    print('EV/EBITDA:', variable.ev_to_ebitda_ratio)
    print('Sales past 3Y:', variable.revenue_growth_3y)
    print()
