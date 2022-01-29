from ETF import ETF
from Stock import Stock


'''
Stock & ETF Columns:
'Ticker', 'Type'
'EV/GP', 'EV/EBIT'
'Median Rev Growth 3Y'

Stock Columns:
'Ticker', 'Type', 'Weight', 'Price', 'Market Cap', 'Enterprise Value', 'Shares Outstanding'
'Revenue', 'Gross Profit', 'EBITDA', 'EBIT', 'Net Income'
'EV/GP', 'EV/EBITDA', 'EV/EBIT', 'Adj EV/EBIT'
'Sales Growth 3Y', 'Median Rev Growth 3Y', 'Median Rev Growth'
'Gross Margin', 'EBITDA Margin', 'EBIT Margin', 'Net Margin'
'Cash', 'Long Term Debt', 'Debt/EBIT', 'Debt/GP', 'R&D', 'R&D/Revenue'
'Share Count Growth 3Y', 'Beta', 'GP/Employees', 'Dividend %'
'Perf Year', 'SMA200', '52W High'
Stock only Columns:

ETF Columns:
'Weighted Median EV/GP', 'Weighted Median EV/EBIT'
'Weighted Median Median Rev Growth 3Y'
'''

etf = ETF('aapl msft amzn googl shop coin pltr')
columns = ['Ticker', 'Type', 'Median Rev Growth 3Y', 'Median Rev Growth', 'EV/GP', 'EV/EBIT']
# columns = ['Ticker', 'Type', 'Sales Growth 3Y', 'Median Rev Growth 3Y', 'EV/GP', 'Adj EV/EBIT', 'Cash', 'Long Term Debt', 'Debt/GP', 'Dividend %', 'Share Count Growth 3Y', 'SMA200', '52W High', 'Perf Year']
etf.display_metrics(columns, only_nums=True)

'''
# Multiple ETF Analysis
#tickers = ['arkk', 'bulz', 'fngg', 'fngu', 'tecl', 'qqq', 'spy', 'vti']
#tickers = ['qqq', 'qld', 'tqqq']  # 1x, 2x, 3x comparison
#tickers = ['spy', 'sso', 'upro']  # 1x, 2x, 3x comparison
#tickers = ['iyw', 'rom', 'tecl']  # 1x, 2x, 3x comparison
#tickers = ['arkk', 'arkw', 'arkg', 'arkf', 'arkq', 'arkx']  # ARK invest ETFs
tickers = ['qqq', 'fngg', 'fngs', 'voo', 'vti', 'spy', 'rom', 'iyw']
for ticker in tickers:
    etf = ETF(ticker)
    print(ticker)
    #print(etf.holdings)
    print(etf.weighted_EV_to_EBITDA_ratio)
    print(etf.weighted_revenue_growth_3y)
    print()
'''
