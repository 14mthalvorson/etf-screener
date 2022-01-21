import requests
import re
from Stock import *


class ETF:

    def __init__(self, ticker):
        self.ticker = ticker
        self.holdings = None

        if ' ' in self.ticker:
            self.set_holdings_from_string(self.ticker)
            self.ticker = 'custom'

        elif self.ticker == 'op' or self.ticker == 'ebitda':  # EBITDA/Operating profit relevant stocks
            ticker_string = 'amzn aapl googl fb cost wmt unh shop tgt meli dis low ups pins roku upst nke hd acn ibm ' \
                            'adsk mime dpz tyl logi hon pypl amd cvx t etsy morn mdt ttd pg mrk ttwo intu abt vmw cmcsa ' \
                            'jnj veev csco mtch amat pfe lrcx zm tmo ko anet orcl qcom anss vz adi isrg akam ms ' \
                            'dsgx adbe irm intc coin eqix pm acc awk mu spgi txn dlr mcd avgo amt cci ma sbac o mrna vrsn ' \
                            'v nvda tsla msft tsm'
            self.set_holdings_from_string(ticker_string)

        elif self.ticker == 'gp' or self.ticker == 'all':  # GP relevant companies
            ticker_string = 'amzn aapl googl fb nflx nvda tsla msft tsm v ma adbe dis crm pypl shop se now snow abnb team ' \
                            'sq snap wsay coin zm ddog twlo ttd crwd net zs veev u pltr twtr hubs okta etsy bill pins tyl ' \
                            'hood rng zen coup open appf amd mu intc intu isrg cost wmt tgt qcom avgo cmcsa psp' \
                            'txn hon amat lrcx adi orcl ibm adsk hd xom mrna pfe jnj pg unh roku brk.b jpm bac nke tmo ' \
                            'csco ko acn abt cvx vz t tmus wfcmcd dpz ups mrk low ms gs mdt pm tdoc morn sbac dlr amt ' \
                            'eqix cci we apps gtlb sofi upst path mttr upwk ai docu fvrr sklz cour appn jamf rblx ' \
                            'cpng spot meli rdfn vmw api cvna avlr dsgx lmnd asan frog zg domo eght mtch bl akam estc ' \
                            'ttwo anss acc anet axp o pton wix irm bmy panw plan vrsn splk spgi pd cybr smar rpd band ' \
                            'fivn mime logi awk qtwo evbg newr mdb mrvl'
            self.set_holdings_from_string(ticker_string)

        elif self.ticker == 'mine':  # My Holdings
            ticker_string = 'amzn etsy tdoc coin fb hood pltr pins sq shop ma aapl nflx nvda tsla v googl amd msft wm mu ' \
                            'crm pypl adbe hubs aappf chgg team zen ttd twlo mdb rng okta payc evbg qtwo veev newr crwd ' \
                            'awk cost logi mime zs fivn smar band rpd cybr pd tyl dis spgi dpz cmcsa ddog qcom avgo splk ' \
                            'plan panw vrsn bmy irm pdi pton zm wix axp csco o z anet now anss soxx snap tdoc arkk arkw ' \
                            'arkg arkf ttwo clou coup bill estc akam bl wday twtr mtch fngu eght domo net apps se api zg ' \
                            'frog snow pltr asan wcld lmnd cvna avlr dsgx abnb ibb idna xbi open qqq vmw tsm rdfn adsk ' \
                            'ter meli u spot roku cpng rblx sumo jamf dt cdns appn tenb glob cour sklz fvrr mrna docu ai ' \
                            'coin mrvl upwk googl mttr meta tqqq path sofi qld usd fngg fngo gtlb we upro rom bulz tmf ' \
                            'ltpz amt cci eqix dlr sbac vpn tyd vig vpu morn edv abt'
            self.set_holdings_from_string(ticker_string)

        elif self.ticker == 'mega':  # Mega-cap tech stocks
            ticker_string = 'amzn aapl googl fb nflx nvda tsla msft tsm'
            self.set_holdings_from_string(ticker_string)

        elif self.ticker == 'reit':  # Digital REIT stocks
            ticker_string = 'sbac dlr eqix amt acc o cci irm'
            self.set_holdings_from_string(ticker_string)

        else:
            self.holdings = self.fill_holdings_from_marketwatch()

        self.weighted_revenue_growth = self.calculate_weighted_revenue_growth()
        self.weighted_revenue_growth_3y = None
        self.weighted_EV_to_EBITDA_ratio = None
        self.calculate_weighted_growth_and_valuation_metrics()

    def fill_holdings_from_marketwatch(self):

        # Retrieve URL from dictionary
        url = 'https://www.marketwatch.com/investing/fund/%s/holdings' % self.ticker

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

    def calculate_weighted_ev_ebitda_ratio(self):
        pass

    def calculate_weighted_ev_gp_ratio(self):
        pass

    def calculate_weighted_revenue_growth(self):
        weighted_numer = 0
        weighted_denom = 0

        for ticker in self.holdings.keys():
            try:
                stock = Stock(ticker)

                if stock.revenue_growth_yoy is not None:
                    weighted_numer += to_number(stock.revenue_growth_yoy) * to_number(self.holdings[ticker])
                    weighted_denom += to_number(self.holdings[ticker])

            except OverflowError:
                pass

            except Exception as e:
                #print('passing on:', ticker, "(weighted revenue growth)", e)
                pass

        if weighted_denom != 0:
            return to_percent_string(weighted_numer / weighted_denom)
        else:
            return None

    def calculate_weighted_growth_and_valuation_metrics(self):
        weighted_ev_to_ebitda = 0
        weighted_revenue_growth_3y = 0
        weighted_denom = 0

        for ticker in self.holdings.keys():
            try:
                stock = Stock(ticker)

                # Ignore outliers above 100% 3Y revenue growth
                if stock.revenue_growth_3y is not None and to_number(stock.revenue_growth_3y) < 1.00 and stock.ev_to_ebitda_ratio is not None and to_number(stock.ev_to_ebitda_ratio) > 0:
                    weighted_revenue_growth_3y += to_number(stock.revenue_growth_3y) * to_number(self.holdings[ticker])
                    weighted_ev_to_ebitda += to_number(stock.ev_to_ebitda_ratio) * to_number(self.holdings[ticker])
                    weighted_denom += to_number(self.holdings[ticker])

            except OverflowError:
                pass

            except Exception as e:
                # Some companies don't have this. That is fine. Don't really need to notify.
                pass

        if weighted_denom != 0:
            self.weighted_revenue_growth_3y = to_percent_string(weighted_revenue_growth_3y / weighted_denom)
            self.weighted_EV_to_EBITDA_ratio = to_ratio_string(weighted_ev_to_ebitda / weighted_denom)
            return
        else:
            self.weighted_revenue_growth_3y = None
            self.weighted_EV_to_EBITDA_ratio = None
            return

    # For each stock in an ETF, displays data selected in metrics
    def display_metrics(self, columns):

        header = ''
        for metric_title in columns:
            header += metric_title + '\t'
        print(header)

        for ticker in self.holdings.keys():
            try:
                stock = Stock(ticker)
                line = ''

                for metric_title in columns:
                    try:
                        if metric_title == 'Ticker':
                            line += stock.ticker + '\t'
                        if metric_title == 'Sales Growth 3Y':
                            line += stock.revenue_growth_3y + '\t'
                        if metric_title == 'Median Rev Growth 3Y':
                            line += stock.med_rev_growth_3y + '\t'
                        if metric_title == 'EV/EBITDA':
                            line += stock.ev_to_ebitda_ratio + '\t'
                        if metric_title == 'EV/GP':
                            line += stock.ev_to_gp_ratio + '\t'
                        if metric_title == 'EV/OP':
                            line += stock.ev_to_op_ratio + '\t'
                        if metric_title == 'Adj EV/OP':
                            line += stock.adj_ev_to_op_ratio + '\t'
                        if metric_title == 'EBITDA Margin':
                            line += stock.ebitda_margin + '\t'
                        if metric_title == 'Gross Margin':
                            line += stock.gross_margin + '\t'
                        if metric_title == 'Operating Margin':
                            line += stock.operating_margin + '\t'
                        if metric_title == 'Net Margin':
                            line += stock.profit_margin + '\t'
                        if metric_title == 'Beta':
                            line += stock.beta + '\t'
                        if metric_title == 'GP/Employees':
                            line += stock.gross_profit_per_employee + '\t'
                        if metric_title == '52W High':
                            line += stock.high_52W + '\t'
                        if metric_title == 'Weighting':
                            line += self.holdings[stock.ticker] + '\t'
                    except Exception as e:
                        line += '' + '\t'
                print(line)

            except OverflowError:
                pass
            except Exception as e:
                pass
