import requests
import re
from Stock import *


class ETF:

    def __init__(self, ticker):
        self.etf_ticker = ticker
        self.ticker_list = None

        if ' ' in self.etf_ticker:
            self.set_holdings_from_string(ticker)
            self.etf_ticker = 'custom'

        # Only include in the list if evaluating this stock with this metric is a decent valuation method.
        elif self.etf_ticker == 'ebitda':  # EBITDA relevant stocks
            ticker_string = 'amzn aapl googl fb cost wmt unh shop tgt meli dis low ups pins roku upst nke hd acn ibm ' \
                            'adsk mime dpz tyl logi hon pypl amd cvx t etsy morn mdt ttd pg mrk ttwo intu abt vmw cmcsa ' \
                            'jnj veev csco mtch amat pfe lrcx zm tmo ko anet orcl qcom anss vz adi isrg akam ms ' \
                            'dsgx adbe irm intc coin eqix pm acc awk mu spgi txn dlr mcd avgo amt cci ma sbac o vrsn ' \
                            'v nvda tsla msft tsm wm now dt cdns'
            self.set_holdings_from_string(ticker_string)

        elif self.etf_ticker == 'op' or self.etf_ticker == 'ebit':  # Operating profit relevant stocks
            ticker_string = 'amzn aapl googl fb cost wmt unh tgt dis low ups pins roku upst nke hd acn ibm ' \
                            'adsk dpz tyl logi hon pypl amd cvx t etsy morn mdt ttd pg mrk ttwo intu abt vmw cmcsa ' \
                            'jnj veev csco mtch amat pfe lrcx zm tmo ko anet orcl qcom anss vz adi isrg akam ms ' \
                            'dsgx adbe irm intc coin eqix pm acc awk mu spgi txn dlr mcd avgo amt cci ma sbac o vrsn ' \
                            'v nvda msft tsm nflx wm dt cdns'
            self.set_holdings_from_string(ticker_string)

        elif self.etf_ticker == 'gp' or self.etf_ticker == 'all':  # GP relevant companies
            ticker_string = 'amzn aapl googl fb nflx nvda tsla msft tsm v ma adbe dis crm pypl shop se now snow abnb team ' \
                            'sq snap wsay coin zm ddog twlo ttd crwd net zs veev u pltr twtr hubs okta etsy bill pins tyl ' \
                            'hood rng zen coup open appf amd mu intc intu isrg cost wmt tgt qcom avgo cmcsa psp' \
                            'txn hon amat lrcx adi orcl ibm adsk hd xom mrna pfe jnj pg unh roku brk.b jpm bac nke tmo ' \
                            'csco ko acn abt cvx vz t tmus wfcmcd dpz ups mrk low ms gs mdt pm tdoc morn sbac dlr amt ' \
                            'eqix cci we apps gtlb sofi upst path mttr upwk ai docu fvrr sklz cour appn jamf rblx ' \
                            'cpng spot meli rdfn vmw api cvna avlr dsgx lmnd asan frog zg domo eght mtch bl akam estc ' \
                            'ttwo anss acc anet axp o pton wix irm bmy panw plan vrsn splk spgi pd cybr smar rpd band ' \
                            'fivn mime logi awk qtwo evbg newr mdb mrvl etsy wm chgg payc wday ter sumo dt cdns tenb glob'
            self.set_holdings_from_string(ticker_string)

        elif self.etf_ticker == 'mine':  # My Holdings
            ticker_string = 'amzn etsy tdoc fb hood pltr pins sq shop ma aapl nflx nvda tsla v googl amd msft wm mu ' \
                            'crm pypl adbe hubs appf chgg team zen ttd twlo mdb rng okta payc evbg qtwo veev newr crwd ' \
                            'awk cost logi mime zs fivn smar band rpd cybr pd tyl dis spgi dpz cmcsa ddog qcom avgo splk ' \
                            'plan panw vrsn bmy irm pdi pton zm wix axp csco o anet now anss soxx snap arkk arkw ' \
                            'arkg arkf ttwo clou coup bill estc akam bl wday twtr mtch fngu eght domo net apps se api zg ' \
                            'frog snow asan wcld lmnd cvna avlr dsgx abnb ibb idna xbi open qqq vmw tsm rdfn adsk ' \
                            'ter meli u spot roku cpng rblx sumo jamf dt cdns appn tenb glob cour sklz fvrr mrna docu ai ' \
                            'coin mrvl upwk mttr meta tqqq path sofi qld usd fngg fngo gtlb we upro rom bulz tmf ' \
                            'ltpz amt cci eqix dlr sbac vpn tyd vig vpu morn edv abt'
            self.set_holdings_from_string(ticker_string)

        elif self.etf_ticker == 'mega':  # Mega-cap tech stocks
            ticker_string = 'amzn aapl googl fb nflx nvda tsla msft tsm'
            self.set_holdings_from_string(ticker_string)

        elif self.etf_ticker == 'reit':  # Digital REIT stocks
            ticker_string = 'sbac dlr eqix amt acc o cci irm'
            self.set_holdings_from_string(ticker_string)

        else:
            self.holdings = self.fill_holdings_from_marketwatch()

        self.stocks = {}
        for ticker in self.holdings.keys():
            try:
                self.stocks[ticker] = Stock(ticker)
            except Exception as e:
                pass

    def fill_holdings_from_marketwatch(self):

        # Retrieve URL from dictionary
        url = 'https://www.marketwatch.com/investing/fund/%s/holdings' % self.etf_ticker

        # Get HTML from URL
        html_doc = requests.get(url).text

        # Regex for pulling tickers
        ticker_results = re.findall('(?<=<td class="table__cell u-semi">)([A-Z]+)(?=<\/td>)', html_doc)

        # Regex for pulling the weightings
        weightings_results = re.findall('(?<=<td class="table__cell">)([0-9]{1,3}.[0-9]{2}%)(?=<\/td>)', html_doc)

        # Get to use dictionary comprehension!!!
        weighted_holdings = {ticker_results[i]: weightings_results[i] for i in range(len(ticker_results))}

        return weighted_holdings

    # Takes space delimited list of tickers and set equal-weight holdings
    def set_holdings_from_string(self, ticker_string):
        self.holdings = {ticker: '1.00%' for ticker in ticker_string.lower().split(' ')}

    # For each stock in an ETF, displays data selected in columns
    def display_metrics(self, columns, only_nums=False):
        header = ''
        for metric_title in columns:
            header += metric_title + '\t'
        print(header)

        for ticker in self.stocks.keys():
            try:
                stock = self.stocks[ticker]
                line = ''

                for metric_title in columns:
                    try:
                        if metric_title == 'Ticker':
                            line += stock.ticker + '\t'
                        if metric_title == 'Weighting':
                            line += self.holdings[stock.ticker] + '\t'
                        if metric_title == 'Price':
                            line += stock.price + '\t'
                        if metric_title == 'Market Cap':
                            line += stock.market_cap + '\t'
                        if metric_title == 'Enterprise Value':
                            line += stock.enterprise_value + '\t'
                        if metric_title == 'Shares Outstanding':
                            line += stock.shares + '\t'

                        if metric_title == 'Revenue':
                            line += stock.revenue + '\t'
                        if metric_title == 'Gross Profit':
                            line += stock.gross_profit + '\t'
                        if metric_title == 'EBITDA':
                            line += stock.ebitda + '\t'
                        if metric_title == 'EBIT':
                            line += stock.ebit + '\t'
                        if metric_title == 'Net Income':
                            line += stock.net_income + '\t'

                        if metric_title == 'EV/GP':
                            line += stock.ev_to_gp_ratio + '\t'
                        if metric_title == 'EV/EBITDA':
                            line += stock.ev_to_ebitda_ratio + '\t'
                        if metric_title == 'EV/EBIT':
                            line += stock.ev_to_op_ratio + '\t'
                        if metric_title == 'Adj EV/EBIT':
                            line += stock.adj_ev_to_ebit_ratio + '\t'

                        if metric_title == 'Sales Growth 3Y':
                            line += stock.revenue_growth_3y + '\t'
                        if metric_title == 'Median Rev Growth 3Y':
                            line += stock.med_rev_growth_3y + '\t'

                        if metric_title == 'Gross Margin':
                            line += stock.gross_margin + '\t'
                        if metric_title == 'EBITDA Margin':
                            line += stock.ebitda_margin + '\t'
                        if metric_title == 'EBIT Margin':
                            line += stock.ebit_margin + '\t'
                        if metric_title == 'Net Margin':
                            line += stock.net_margin + '\t'

                        if metric_title == 'Cash':
                            line += stock.cash + '\t'
                        if metric_title == 'Long Term Debt':
                            line += stock.long_term_debt + '\t'
                        if metric_title == 'Debt/EBIT':
                            line += stock.debt_to_ebit + '\t'
                        if metric_title == 'R&D':
                            line += stock.research_development + '\t'
                        if metric_title == 'R&D/Revenue':
                            line += stock.research_over_revenue + '\t'

                        if metric_title == 'Share Count Growth 3Y':
                            line += stock.share_count_growth_3y + '\t'
                        if metric_title == 'Beta':
                            line += stock.beta + '\t'
                        if metric_title == 'GP/Employees':
                            line += stock.gross_profit_per_employee + '\t'
                        if metric_title == '52W High':
                            line += stock.high_52W + '\t'

                    except Exception as e:
                        line += '' + '\t'

                if only_nums:
                    line = ''.join(x for x in line if x not in 'BMK')
                print(line)

            except OverflowError:
                pass
            except Exception as e:
                pass
