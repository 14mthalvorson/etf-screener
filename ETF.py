import requests
import re
from utilities import *
from Stock import Stock
from finviz_finance_fulfillment import get_finviz_metrics


class ETF:

    # Ticker can be an ETF ticker
    # Ticker can also be a string of ETF and Stock tickers (separated by a space) (many examples below)
    def __init__(self, ticker):
        self.components = {}  # HashMap[ticker]: Stock or ETF
        self.weights = None  # HashMap[ticker]: weight
        self.ticker_string = None  # String of component tickers separated by a space
        self.ticker = None  # Name/Ticker of this ETF
        self.type = 'ETF'
        self.is_real_etf = False

        # Set ticker_string
        if ' ' in ticker:
            self.ticker_string = ticker
            ticker = 'custom'

        # Only include in the list if evaluating this stock with this metric is a decent valuation method.
        elif ticker == 'ebitda':  # EBITDA relevant stocks
            self.ticker_string = 'amzn aapl googl fb cost wmt unh shop tgt meli dis low ups pins roku upst nke hd acn ibm ' \
                            'adsk mime dpz tyl logi hon pypl amd cvx t etsy morn mdt ttd pg mrk ttwo intu abt vmw cmcsa ' \
                            'jnj veev csco mtch amat pfe lrcx zm tmo ko anet orcl qcom anss vz adi isrg akam ms ' \
                            'dsgx adbe irm intc coin eqix pm acc awk mu spgi txn dlr mcd avgo amt cci ma sbac o vrsn ' \
                            'v nvda tsla msft tsm wm now dt cdns'

        elif ticker == 'op' or ticker == 'ebit':  # Operating profit relevant stocks
            self.ticker_string = 'amzn aapl googl fb cost wmt unh tgt dis low ups pins roku upst nke hd acn ibm ' \
                            'adsk dpz tyl logi hon pypl amd cvx t etsy morn mdt ttd pg mrk ttwo intu abt vmw cmcsa ' \
                            'jnj veev csco mtch amat pfe lrcx zm tmo ko anet orcl qcom anss vz adi isrg akam ms ' \
                            'dsgx adbe irm intc coin eqix pm acc awk mu spgi txn dlr mcd avgo amt cci ma sbac o vrsn ' \
                            'v nvda msft tsm nflx wm dt cdns'

        elif ticker == 'gp' or ticker == 'all':  # GP relevant companies
            self.ticker_string = 'amzn aapl googl fb nflx nvda tsla msft tsm v ma adbe dis crm pypl shop se now snow abnb team ' \
                            'sq snap wsay coin zm ddog twlo ttd crwd net zs veev u pltr twtr hubs okta etsy bill pins tyl ' \
                            'hood rng zen coup open appf amd mu intc intu isrg cost wmt tgt qcom avgo cmcsa psp' \
                            'txn hon amat lrcx adi orcl ibm adsk hd xom mrna pfe jnj pg unh roku brk.b jpm bac nke tmo ' \
                            'csco ko acn abt cvx vz t tmus wfcmcd dpz ups mrk low ms gs mdt pm tdoc morn sbac dlr amt ' \
                            'eqix cci we apps gtlb sofi upst path mttr upwk ai docu fvrr sklz cour appn jamf rblx ' \
                            'cpng spot meli rdfn vmw api cvna avlr dsgx lmnd asan frog zg domo eght mtch bl akam estc ' \
                            'ttwo anss acc anet axp o pton wix irm bmy panw plan vrsn splk spgi pd cybr smar rpd band ' \
                            'fivn mime logi awk qtwo evbg newr mdb mrvl etsy wm chgg payc wday ter sumo dt cdns tenb glob'

        elif ticker == 'mine':  # My Holdings
            self.ticker_string = 'amzn etsy tdoc fb hood pltr pins sq shop ma aapl nflx nvda tsla v googl amd msft wm mu ' \
                            'crm pypl adbe hubs appf chgg team zen ttd twlo mdb rng okta payc evbg qtwo veev newr crwd ' \
                            'awk cost logi mime zs fivn smar band rpd cybr pd tyl dis spgi dpz cmcsa ddog qcom avgo splk ' \
                            'plan panw vrsn bmy irm pdi pton zm wix axp csco o anet now anss soxx snap arkk arkw ' \
                            'arkg arkf ttwo clou coup bill estc akam bl wday twtr mtch fngu eght domo net apps se api zg ' \
                            'frog snow asan wcld lmnd cvna avlr dsgx abnb ibb idna xbi open qqq vmw tsm rdfn adsk ' \
                            'ter meli u spot roku cpng rblx sumo jamf dt cdns appn tenb glob cour sklz fvrr mrna docu ai ' \
                            'coin mrvl upwk mttr meta tqqq path sofi qld usd fngg fngo gtlb we upro rom bulz tmf ' \
                            'ltpz amt cci eqix dlr sbac vpn tyd vig vpu morn edv abt'

        elif ticker == 'market_cap':  # GP relevant companies
            self.ticker_string = 'aapl msft googl amzn tsla fb brk.b tsm nvda v jnj jpm unh wmt pg bac hd baba ma tm xom pfe ' \
                            'asml dis ko cvx adbe csco abbv pep nke cmcsa lly tmo avgo acn orcl vz wfc abt crm cost nvs ' \
                            'nflx intc mrk pypl dhr t qcom mcd azn ms ups nvo schw bbl bhp sap lin ry txn pm unp low ' \
                            'tte intu nee td hsbc sony hon bmy mdt axp amd cvs rtx ul tmus bx sny shop c amgn blk ' \
                            'ba rio ibm amat cop jd cat deo gs amt bud de sbux pld lfc gsk hdb antm lmt el bp tgt isrg ' \
                            'ge chtr mmm now bkng infy bti eqnr spgi syk mu zts adp mdlz mo abnb pnc se usb bns cni ' \
                            'bam tfc gild enb lrcx cb f pbr adi snow tjx cme vale mufg mmc ci pdd cci shw duk csx ' \
                            'gm bmo ibn'

        elif ticker == 'revenue':  # GP relevant companies
            self.ticker_string = 'wmt amzn aapl unh cvs tm xom googl cost msft t ci tte hd jd cvx f lfc vz antm bp gm ' \
                            'cmcssa fb tgt low ups jnj sony tmus intc pg pep ge ibm bam pfe eqnr dis lmt gs rtx ba ' \
                            'ms bhp rio jpm tsm ul bbl vale abbv acn bud nvs chtr csco c cat mrk bac tsla nke tjx bmy'

        elif ticker == 'ETFs':  # Popular ETFs
            self.ticker_string = 'qqq spy arkk'

        elif ticker == 'LETFs':  # Leveraged ETFs
            self.ticker_string = 'qqq qld tqqq tecl bulz rom fngu upro sso fngg iyw fngo fngs spy vpn'

        elif ticker == 'mega':  # Mega-cap tech stocks
            self.ticker_string = 'aapl amzn googl fb nflx nvda tsla msft tsm'

        elif ticker == 'reit':  # Digital REIT stocks
            self.ticker_string = 'sbac dlr eqix amt acc o cci irm'

        # Set weights and ticker_string if not set
        if self.ticker_string is None:  # Actual ETF name was provided
            self.is_real_etf = True
            self.fill_holdings_from_marketwatch(ticker)
            self.ticker_string = ' '.join(list(self.weights.keys()))
        else:
            self.weights = {ticker: '1.00%' for ticker in self.ticker_string.split(' ')}

        # Set ticker
        self.ticker = ticker

        # Set components
        self.set_components()

        # Query Finviz metrics for real ETFs
        if self.is_real_etf:
            finviz_fundamentals = get_finviz_metrics(ticker, ['Dividend %', 'Price', 'SMA200', '52W High', 'Perf Year'])

            self.dividend_yield = finviz_fundamentals['Dividend %']
            self.price = finviz_fundamentals['Price']
            self.sma200 = finviz_fundamentals['SMA200']
            self.high_52W = finviz_fundamentals['52W High']
            self.perf_year = finviz_fundamentals['Perf Year']

        # Calculate additional metrics based on components and weights

        # Weighted Median Enterprise Value
        relative_EVs = []
        for ticker in self.weights.keys():
            try:
                for i in range(int(to_number(self.weights[ticker]) * 100)):
                    relative_EVs.append(self.components[ticker].enterprise_value)
            except Exception as e:
                pass
        try:
            self.weighted_median_EV = get_median_from_list(relative_EVs)
        except Exception as e:
            self.weighted_median_EV = None

        # Weighted Median EV/GP
        relative_EV_to_GPs = []
        for ticker in self.weights.keys():
            try:
                for i in range(int(to_number(self.weights[ticker]) * 100)):
                    relative_EVs.append(self.components[ticker].ev_to_gp_ratio)
            except Exception as e:
                pass
        try:
            self.weighted_median_EV_to_GP = get_median_from_list(relative_EV_to_GPs)
        except Exception as e:
            self.weighted_median_EV_to_GP = None

    def fill_holdings_from_marketwatch(self, ticker):
        # Retrieve URL from dictionary
        url = 'https://www.marketwatch.com/investing/fund/%s/holdings' % ticker
        html_doc = requests.get(url).text
        # Regex for pulling tickers
        ticker_results = re.findall('(?<=<td class="table__cell u-semi">)([A-Z]+)(?=<\/td>)', html_doc)
        # Regex for pulling the weightings
        weightings_results = re.findall('(?<=<td class="table__cell">)([0-9]{1,3}.[0-9]{2}%)(?=<\/td>)', html_doc)
        # Get to use dictionary comprehension!!!
        self.weights = {ticker_results[i]: weightings_results[i] for i in range(len(ticker_results))}
        return

    # Takes space delimited list of tickers and set equal-weight holdings
    def set_components(self):
        for ticker in self.weights.keys():
            try:  # Try to make the ticker a stock. If it is likely not a stock, it is probably an ETF.
                self.components[ticker] = Stock(ticker)
                if self.components[ticker].type == 'ETF':
                    self.components[ticker] = ETF(ticker)
            except Exception as e:
                pass

    # For each stock in an ETF, displays data selected in columns
    def display_metrics(self, columns, only_nums=False):
        header = ''
        for metric_title in columns:
            header += metric_title + '\t'
        print(header)

        for ticker in self.components.keys():
            try:
                component = self.components[ticker]  # Either a stock or an ETF
                line = ''

                for metric_title in columns:
                    try:
                        if metric_title == 'Ticker':
                            line += component.ticker + '\t'
                        if metric_title == 'Type':
                            line += component.type + '\t'
                        if metric_title == 'Weight':
                            line += self.weights[component.ticker] + '\t'
                        if metric_title == 'Price':
                            line += component.price + '\t'
                        if metric_title == 'Market Cap':
                            line += component.market_cap + '\t'
                        if metric_title == 'Enterprise Value':
                            line += component.enterprise_value + '\t'
                        if metric_title == 'Shares Outstanding':
                            line += component.shares + '\t'

                        if metric_title == 'Revenue':
                            line += component.revenue + '\t'
                        if metric_title == 'Gross Profit':
                            line += component.gross_profit + '\t'
                        if metric_title == 'EBITDA':
                            line += component.ebitda + '\t'
                        if metric_title == 'EBIT':
                            line += component.ebit + '\t'
                        if metric_title == 'Net Income':
                            line += component.net_income + '\t'

                        if metric_title == 'EV/GP':
                            line += component.ev_to_gp_ratio + '\t'
                        if metric_title == 'EV/EBITDA':
                            line += component.ev_to_ebitda_ratio + '\t'
                        if metric_title == 'EV/EBIT':
                            line += component.ev_to_op_ratio + '\t'
                        if metric_title == 'Adj EV/EBIT':
                            line += component.adj_ev_to_ebit_ratio + '\t'

                        if metric_title == 'Sales Growth 3Y':
                            line += component.revenue_growth_3y + '\t'
                        if metric_title == 'Median Rev Growth 3Y':
                            line += component.med_rev_growth_3y + '\t'

                        if metric_title == 'Gross Margin':
                            line += component.gross_margin + '\t'
                        if metric_title == 'EBITDA Margin':
                            line += component.ebitda_margin + '\t'
                        if metric_title == 'EBIT Margin':
                            line += component.ebit_margin + '\t'
                        if metric_title == 'Net Margin':
                            line += component.net_margin + '\t'

                        if metric_title == 'Cash':
                            line += component.cash + '\t'
                        if metric_title == 'Long Term Debt':
                            line += component.long_term_debt + '\t'
                        if metric_title == 'Debt/GP':
                            line += component.debt_to_gp + '\t'
                        if metric_title == 'Debt/EBIT':
                            line += component.debt_to_ebit + '\t'
                        if metric_title == 'R&D':
                            line += component.research_development + '\t'
                        if metric_title == 'R&D/Revenue':
                            line += component.research_over_revenue + '\t'

                        if metric_title == 'Dividend %':
                            line += component.dividend_yield + '\t'
                        if metric_title == 'Share Count Growth 3Y':
                            line += component.share_count_growth_3y + '\t'
                        if metric_title == 'Beta':
                            line += component.beta + '\t'
                        if metric_title == 'GP/Employees':
                            line += component.gross_profit_per_employee + '\t'

                        if metric_title == '52W High':
                            line += component.high_52W + '\t'
                        if metric_title == 'Perf Year':
                            line += component.perf_year + '\t'
                        if metric_title == 'SMA200':
                            line += component.sma200 + '\t'

                        # ETF Only Metrics
                        if metric_title == 'Weighted Median EV':
                            line += component.weighted_median_EV + '\t'
                        if metric_title == 'Weighted Median EV/GP':
                            line += component.weighted_median_EV_to_GP + '\t'

                    except Exception as e:
                        line += '' + '\t'

                if only_nums:
                    line = ''.join(x for i, x in enumerate(line) if i-1 < 0 or x not in 'BMK' or line[i-1] not in '1234567890')
                print(line)

            except OverflowError:
                pass
            except Exception as e:
                pass
