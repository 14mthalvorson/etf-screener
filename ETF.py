class ETF:

    def __init__(self, ticker):
        self.ticker = ticker
        self.holdings = None

        finviz_fundamentals = get_finviz_metrics(ticker,
                                                 ['Company', 'Price', 'Market Cap', 'Sales', 'Dividend %', 'P/E', 'P/S',
                                                  'EPS this Y', 'Sales Q/Q', 'Sales past 5Y', 'Gross Margin',
                                                  'Oper. Margin', 'Profit Margin', 'SMA200', '52W High', '52W Low',
                                                  'Perf Year'])

        if ticker == 'qqq':
            self.fill_qqq_holdings()

    # Holdings is a dictionary of weighted holdings
    def __int__(self, ticker, holdings):
        self = ETF()
        self.holdings = holdings

    def set_holdings(self, holdings):
        self.holdings = holdings

    def fill_holdings_from_marketwatch(self):

        # Retrieve URL from dictionary
        url = 'https://www.marketwatch.com/investing/fund/qqq/holdings'

        # Get HTML from URL
        html_doc = requests.get(url).text

        # Regex for pulling tickers
        ticker_results = re.findall('(?<=<td class="table__cell u-semi">)([A-Z]+)(?=<\/td>)', html_doc)

        # Regex for pulling the weightings
        weightings_results = re.findall('(?<=<td class="table__cell">)([0-9]{1,3}.[0-9]{2}%)(?=<\/td>)', html_doc)

        # Get to use dictionary comprehension!!!
        weighted_holdings = {ticker_results[i]: weightings_results[i] for i in range(len(ticker_results))}

        return weighted_holdings

    def calculate_weighted_ev_ebitda_ratio(self):
        pass

    def calculate_weighted_revenue_growth(self):
        weighted_numer = 0
        weighted_denom = 0

