from ETF import ETF
from Stock import Stock


'''
Stock & ETF Columns:
'Ticker', 'Name', 'Type', 'Weight'
'EV/GP', 'Adj EV/EBIT', 'EV/EBIT'
'Median Rev Growth 3Y'
'Gross Margin', 'Adj EBIT Margin'
'52W High'

Stock Columns:
'Ticker', 'Type', 'Weight', 'Price', 'Market Cap', 'Enterprise Value', 'Shares Outstanding'
'Revenue', 'Gross Profit', 'EBITDA', 'EBIT', 'Net Income'
'EV/GP', 'EV/EBITDA', 'Adj EV/EBIT', 'EV/EBIT'
'Sales Growth 3Y', 'Median Rev Growth 3Y', 'Median Rev Growth'
'Gross Margin', 'EBITDA Margin', 'Adj EBIT Margin', 'EBIT Margin', 'Net Margin'
'Cash', 'Long Term Debt', 'Debt/EBIT', 'Debt/GP', 'R&D', 'R&D/Revenue'
'Share Count Growth 3Y', 'Beta', 'GP/Employees', 'Dividend %'
'Perf Year', 'SMA200', '52W High'

ETF Columns:
'Weighted Median EV/GP', 'Weighted Median Adj EV/EBIT', 'Weighted Median EV/EBIT'
'Weighted Median Median Rev Growth 3Y'
'Weighted Median Gross Margin', 'Weighted Median Adj EBIT Margin'
'''

etf = ETF('spy')
columns = ['Ticker', 'Name', 'Type', 'Median Rev Growth 3Y', 'EV/GP', 'Adj EV/EBIT', 'Gross Margin', 'Adj EBIT Margin', '52W High']
etf.display_metrics(columns, only_nums=True, extra_header=True, include_overall=False)
