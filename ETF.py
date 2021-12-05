class ETF:

    def __init__(self, ticker):
        self.ticker = ticker
        self.holdings = None

        finviz_fundamentals = get_finviz_metrics(ticker,
                                                 ['Company', 'Price', 'Market Cap', 'Sales', 'Dividend %', 'P/E', 'P/S',
                                                  'EPS this Y', 'Sales Q/Q', 'Sales past 5Y', 'Gross Margin',
                                                  'Oper. Margin', 'Profit Margin', 'SMA200', '52W High', '52W Low',
                                                  'Perf Year'])

    # Holdings is a dictionary of weighted holdings
    def __int__(self, ticker, holdings):
        self = ETF()
        self.holdings = holdings

    def set_holdings(self, holdings):
        self.holdings = holdings
