import requests
import re
from utilities import *
from Stock import Stock
from Crypto import Crypto
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
            self.ticker_string = 'aapl abbv abnb abt acc acn adbe adi adp adsk ai akam amat amd amgn amt amzn anet ' \
                                 'anss antm api appf appn apps arkf arkg arkk arkw asan asml avgo avlr awk axp azn ' \
                                 'ba baba bac bam band bbl bhp bill bkng bl blk bmo bmy bns bp brkb bti bud bulz bx ' \
                                 'c cat cb cci cdns chgg chtr ci clou cmcsa cmcssa cme cni coin cop cost coup cour ' \
                                 'cpng crm crwd csco csx cvna cvs cvx cybr ddog de deo dhr dis dlr docu domo dpz ' \
                                 'dsgx dt duk edv eght el enb eqix eqnr estc etsy evbg f fb fivn fngg fngo fngs fngu ' \
                                 'frog fvrr gdxj ge gild glob gm googl gs gsk gtlb hd hdb hon hood hsbc hubs ibb ibm ' \
                                 'ibn infy intc intu irm isrg itb iye iyr iyw jamf jd jnj jpm kbe ko lfc lin lly lmnd ' \
                                 'lmt logi low lrcx ltpz ma mcd mdb mdlz mdt meli meta mime mmc mmm mo moat morn mrk ' \
                                 'mrna mrvl ms msft mtch mttr mu mufg nee net newr nflx nke now nvda nvo nvs o oih ' \
                                 'okta open orcl panw path payc pbr pd pdd pdi pep pfe pg pins plan pld pltr pm pnc ' \
                                 'psp pton pypl qcom qld qqq qtwo rblx rdfn rio rng roku rom rpd rtx ry sap sbac sbux ' \
                                 'schw se shop shw sklz smar smh snap snow sny sofi sony soxx spgi splk spot spy sq ' \
                                 'sso sumo syk t td tdoc team tecl tenb ter tfc tgt tjx tm tmf tmo tmus tqqq tsla tsm ' \
                                 'ttd tte ttwo twlo twtr txn tyd tyl u ul unh unp upro ups upst upwk usb usd v vale ' \
                                 'veev vig vmw vnq vpn vpu vrsn vtv vug vz wcld wday we wfc wfcmcd wix wm wmt wsay ' \
                                 'xbi xhb xlb xle xlf xli xlk xlp xlu xlv xly xme xom xop xrt xtl zen zg zm zs zts '

        elif ticker == 'mine':  # My Holdings
            self.ticker_string = 'aapl abnb abt adbe adsk ai akam amd amt amzn anet anss api appf appn apps arkf ' \
                                 'arkg arkk arkw asan avgo avlr awk axp band bill bl bmy bulz cci cdns chgg clou ' \
                                 'cmcsa coin cost coup cour cpng crm crwd csco cvna cybr ddog dis dlr docu domo dpz ' \
                                 'dsgx dt edv eght eqix estc etsy evbg fb fivn fngg fngo fngu frog fvrr glob googl ' \
                                 'gtlb hood hubs ibb idna irm jamf lmnd logi ltpz ma mdb meli meta metv mime morn ' \
                                 'mrna mrvl msft mtch mttr mu net newr nflx now nvda o okta open panw path payc pd ' \
                                 'pdi pins plan pltr pton pypl qcom qld qqq qtwo rblx rdfn rng roku rom rpd sbac se ' \
                                 'shop sklz smar snap snow sofi soxx spgi splk spot sq sumo tdoc team tenb ter tmf ' \
                                 'tqqq tsla tsm ttd ttwo twlo twtr tyd tyl u upro upwk usd v veev vig vmw vpn vpu ' \
                                 'vrsn wcld wday we wix wm xbi z zen zg zm zs'

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

        elif ticker == 'top_ETFs':  # Popular ETFs
            self.ticker_string = 'spy qqq vtv vug vig arkk moat vpn wcld soxx xlv xlu xlf'

        elif ticker == 'm1_ETFs':  # Popular ETFs
            self.ticker_string = 'qqq spy xlv xlf xlu moat vig soxx'

        elif ticker == 'my_ETFs':  # Popular ETFs
            self.ticker_string = 'spy qqq vtv vug vig arkk moat vpn wcld soxx xlv xlu xlf vpu meta ibb clou xbi arkw arkf arkg'

        elif ticker == 'sector_ETFs':  # Sector ETFs
            self.ticker_string = 'spy qqq vtv vig vpn soxx xle xlf xlu xli xlk xlv xly xlp xlb xop iyr xhb itb vnq gdxj iye oih xme xrt smh ibb kbe xtl'

        elif ticker == 'LETFs':  # Leveraged ETFs
            self.ticker_string = 'qqq qld tqqq tecl bulz rom fngu upro sso fngg iyw fngo fngs spy vpn'

        elif ticker == 'mega':  # Mega-cap tech stocks
            self.ticker_string = 'aapl amzn googl fb nflx nvda tsla msft tsm'

        elif ticker == 'reit':  # Digital REIT stocks
            self.ticker_string = 'sbac dlr eqix amt acc o cci irm'

        elif ticker == 'fngg':  # FNGG ETF Holdings
            self.ticker_string = 'googl amd fb nvda amzn msft aapl nflx rblx zs snap crwd se ddog nio snow u tsla zm shop'

        elif ticker == 'crypto':  # Cryptocurrencies
            self.ticker_string = 'BTCUSD ETHUSD XRPUSD LTCUSD'

        elif ticker == 'qqq':  # Hardcoded more than top 25 QQQ holdings
            self.weights = {'aapl': '11.69%', 'msft': '10.13%', 'googl': '7.19%', 'amzn': '6.78%', 'fb': '4.78%',
                            'tsla': '4.26%', 'nvda': '4.15%', 'avgo': '1.82%', 'adbe': '1.8%', 'csco': '1.78%',
                            'nflx': '1.78%', 'cost': '1.67%', 'pep': '1.6%', 'cmcsa': '1.53%', 'pypl': '1.47%',
                            'intc': '1.39%', 'qcom': '1.36%', 'intu': '1.21%', 'txn': '1.16%', 'amd': '1.16%',
                            'tmus': '0.96%', 'hon': '0.96%', 'amat': '0.95%', 'sbux': '0.91%', 'mu': '0.66%',
                            'adi': '0.64%', 'adp': '0.63%', 'lrcx': '0.59%', 'fisv': '0.52%', 'chtr': '0.79%',
                            'bkng': '0.74%', 'mdlz': '0.69%', 'amgn': '0.96%', 'isrg': '0.73%', 'gild': '0.65%',
                            'csx': '0.57%', 'exc': '0.42%', 'regn': '0.49%', 'mrna': '0.48%', 'vrtx': '0.46%',
                            'kdp': '0.40%', 'meli': '0.40%', 'atvi': '0.46%', 'klac': '0.42%', 'mrvl': '0.41%'}
            self.ticker_string = 'qqq'
            self.is_real_etf = True

        elif ticker == 'spy':  # Hardcoded more than top 25 SPY holdings
            self.weights = {'aapl': '7.12', 'msft': '6.11', 'amzn': '3.41', 'googl': '4.13', 'tsla': '1.99',
                            'fb': '1.94', 'nvda': '1.60', 'brk.b': '1.50', 'jnj': '1.19',
                            'unh': '1.16', 'jpm': '1.15', 'pg': '1.02', 'hd': '1.01', 'v': '0.99', 'ma': '0.88',
                            'bac': '0.87', 'xom': '0.84', 'pfe': '0.77', 'dis': '0.68', 'adbe': '0.66', 'cvx': '0.66',
                            'abbv': '0.63', 'avgo': '0.63', 'pep': '0.63', 'ko': '0.62', 'csco': '0.61', 'tmo': '0.60',
                            'cmcsa': '0.60', 'crm': '0.60', 'abt': '0.59', 'acn': '0.58', 'cost': '0.58', 'vz': '0.58',
                            'wfc': '0.56', 'mrk': '0.54', 'pypl': '0.53', 'wmt': '0.52', 'intc': '0.52', 'qcom': '0.51',
                            'lly': '0.51', 'mcd': '0.51', 'nflx': '0.49', 'nke': '0.49', 'dhr': '0.48', 't': '0.47',
                            'txn': '0.43', 'low': '0.43', 'lin': '0.43', 'pm': '0.42', 'unp': '0.41', 'intu': '0.41',
                            'nee': '0.40', 'ups': '0.39', 'ms': '0.38', 'bmy': '0.38', 'hon': '0.37', 'cvs': '0.37',
                            'mdt': '0.36', 'amd': '0.36', 'rtx': '0.35', 'schw': '0.34', 'orcl': '0.34', 'c': '0.34',
                            'amgn': '0.34', 'amat': '0.33', 'gs': '0.31', 'ibm': '0.31', 'blk': '0.31', 'cop': '0.31',
                            'now': '0.30', 'pld': '0.30', 'sbux': '0.30', 'amt': '0.30', 'axp': '0.30', 'ba': '0.29',
                            'cat': '0.29', 'tgt': '0.28', 'antm': '0.28', 'de': '0.28', 'ge': '0.27', 'isrg': '0.26',
                            'bkng': '0.26', 'spgi': '0.26', 'mmm': '0.25', 'lmt': '0.25', 'zts': '0.25', 'mo': '0.24',
                            'mdlz': '0.24', 'mu': '0.24', 'adi': '0.23', 'pnc': '0.23', 'adp': '0.23', 'tjx': '0.23',
                            'gild': '0.22', 'cb': '0.22', 'tfc': '0.22', 'syk': '0.22', 'lrcx': '0.22', 'cme': '0.22',
                            'duk': '0.21', 'f': '0.21', 'cci': '0.21', 'usb': '0.20', 'mmc': '0.20', 'gm': '0.20',
                            'ci': '0.20', 'csx': '0.20'}
            self.ticker_string = 'spy'
            self.is_real_etf = True

        elif ticker == 'vig':  # Hardcoded more than top 25 VIG holdings
            self.weights = {'msft': '4.83%', 'unh': '3.76%', 'jnj': '3.58%', 'hd': '3.47%', 'jpm': '3.31%',
                            'pg': '3.16%', 'v': '2.77%', 'avgo': '2.15%', 'acn': '2.07%', 'cost': '1.98%',
                            'abt': '1.97%', 'pep': '1.91%', 'ko': '1.82%', 'cmcsa': '1.82%', 'nke': '1.67%',
                            'wmt': '1.63%', 'qcom': '1.62%', 'mcd': '1.59%', 'nee': '1.45%', 'low': '1.42%',
                            'lin': '1.41%', 'txn': '1.38%', 'unp': '1.29%', 'ups': '1.23%', 'hon': '1.15%',
                            'orcl': '1.14%', 'bmy': '1.11%', 'mdt': '1.10%', 'sbux': '1.09%', 'blk': '1.04%',
                            'spgi': '0.90%', 'tgt': '0.90%', 'cat': '0.88%', 'adp': '0.83%', 'mmm': '0.81%',
                            'adi': '0.75%', 'syk': '0.71%', 'mmc': '0.69%', 'lmt': '0.69%', 'shw': '0.68%',
                            'pnc': '0.67%', 'csx': '0.66%', 'cb': '0.66%', 'cme': '0.65%', 'tfc': '0.62%',
                            'cl': '0.58%', 'bdx': '0.57%', 'itw': '0.56%', 'etn': '0.55%', 'apd': '0.53%',
                            'klac': '0.52%', 'wm': '0.51%', 'mco': '0.50%', 'ecl': '0.46%', 'noc': '0.46%',
                            'emr': '0.44%', 'tel': '0.42%', 'rop': '0.41%', 'atvi': '0.41%', 'gd': '0.38%'}
            self.ticker_string = 'vig'
            self.is_real_etf = True

        elif ticker == 'vtv':  # Hardcoded more than top 25 VTV holdings
            self.weights = {'brk.b': '2.85%', 'unh': '2.58%', 'jpm': '2.55%', 'jnj': '2.45%', 'pg': '2.16%',
                            'pfe': '1.81%', 'bac': '1.69%', 'avgo': '1.42%', 'xom': '1.41%', 'abt': '1.36%',
                            'csco': '1.31%', 'pep': '1.31%', 'abbv': '1.30%', 'lly': '1.30%', 'ko': '1.25%',
                            'cmcsa': '1.25%', 'cvx': '1.23%', 'intc': '1.14%', 'wmt': '1.10%', 'vz': '1.07%',
                            'mrk': '1.05%', 'wfc': '1.04%', 'nee': '0.97%', 't': '0.96%', 'pm': '0.81%',
                            'hon': '0.78%', 'orcl': '0.78%', 'ms': '0.77%', 'mdt': '0.76%', 'bmy': '0.75%',
                            'cvs': '0.74%', 'schw': '0.71%', 'gs': '0.70%', 'rtx': '0.70%', 'amgn': '0.69%',
                            'blk': '0.68%', 'pld': '0.68%', 'c': '0.65%', 'ibm': '0.63%', 'antm': '0.61%',
                            'cat': '0.61%', 'tgt': '0.60%', 'dhr': '0.58%', 'ge': '0.57%', 'qcom': '0.56%',
                            'mmm': '0.56%', 'de': '0.52%', 'cop': '0.52%', 'axp': '0.52%', 'adi': '0.51%',
                            'mdlz': '0.50%', 'gild': '0.50%', 'bx': '0.48%', 'mmc': '0.48%', 'mo': '0.47%',
                            'pnc': '0.46%', 'csx': '0.45%', 'lmt': '0.45%', 'cme': '0.45%', 'f': '0.44%'}
            self.ticker_string = 'vtv'
            self.is_real_etf = True

        elif ticker == 'xlv':  # Hardcoded more than top 25 XLV (Healthcare) holdings
            self.weights = {'unh': '9.112%', 'jnj': '9.002%', 'pfe': '5.93%', 'abbv': '4.927%', 'tmo': '4.637%',
                            'abt': '4.554%', 'mrk': '3.95%', 'lly': '3.847%', 'dhr': '3.649%', 'cvs': '2.842%',
                            'bmy': '2.815%', 'mdt': '2.72%', 'amgn': '2.498%', 'antm': '2.171%', 'isrg': '2.018%',
                            'zts': '1.882%', 'syk': '1.667%', 'gild': '1.624%', 'bdx': '1.539%', 'ci': '1.427%',
                            'ew': '1.377%', 'regn': '1.299%', 'vrtx': '1.227%', 'bsx': '1.202%', 'mrna': '1.145%',
                            'hca': '1.142%', 'ilmn': '1.103%', 'hum': '1.085%', 'iqv': '0.946%', 'cnc': '0.941%',
                            'idxx': '0.904%', 'bax': '0.852%', 'a': '0.85%', 'mck': '0.808%', 'dxcm': '0.803%',
                            'algn': '0.731%', 'rmd': '0.682%', 'mtd': '0.68%', 'biib': '0.64%', 'wst': '0.589%',
                            'cern': '0.536%', 'lh': '0.527%', 'zbh': '0.502%', 'pki': '0.469%', 'ste': '0.451%',
                            'abc': '0.409%', 'wat': '0.399%', 'coo': '0.381%', 'holx': '0.368%', 'vtrs': '0.362%',
                            'ctlt': '0.347%', 'crl': '0.336%', 'dgx': '0.33%', 'tech': '0.315%', 'tfx': '0.289%',
                            'cah': '0.287%', 'incy': '0.272%', 'bio': '0.265%', 'abmd': '0.262%', 'xray': '0.228%',
                            'hsic': '0.21%', 'uhs': '0.19%', 'ogn': '0.166%', 'dva': '0.142%'}
            self.ticker_string = 'xlv'
            self.is_real_etf = True

        elif ticker == 'xlf':  # Hardcoded more than top 25 XLF (Financials) holdings
            self.weights = {'brk.b': '13.25%', 'jpm': '10.086%', 'bac': '7.675%', 'wfc': '5.049%', 'ms': '3.37%',
                            'schw': '3.067%', 'c': '2.972%', 'gs': '2.796%', 'axp': '2.65%', 'blk': '2.642%',
                            'spgi': '2.285%', 'cb': '2.05%', 'pnc': '2.018%', 'cme': '1.989%', 'tfc': '1.94%',
                            'usb': '1.832%', 'mmc': '1.762%', 'ice': '1.654%', 'pgr': '1.473%', 'cof': '1.449%',
                            'aon': '1.399%', 'mco': '1.263%', 'aig': '1.134%', 'met': '1.112%', 'bk': '1.06%',
                            'msci': '1.022%', 'pru': '0.984%', 'trv': '0.971%', 'afl': '0.891%', 'stt': '0.815%',
                            'sivb': '0.81%', 'all': '0.801%', 'amp': '0.782%', 'dfs': '0.78%', 'trow': '0.763%',
                            'ajg': '0.735%', 'fitb': '0.725%', 'frc': '0.72%', 'wtw': '0.67%', 'ntrs': '0.57%',
                            'hig': '0.564%', 'key': '0.547%', 'syf': '0.531%', 'cfg': '0.518%', 'mtb': '0.517%',
                            'hban': '0.517%', 'rf': '0.516%', 'ndaq': '0.478%', 'rjf': '0.459%', 'sbny': '0.432%',
                            'cinf': '0.414%', 'pfg': '0.411%', 'fds': '0.362%', 'bro': '0.359%', 'mktx': '0.305%',
                            'cma': '0.286%', 'cboe': '0.286%', 'wrb': '0.285%', 'l': '0.281%', 'lnc': '0.262%',
                            're': '0.258%', 'zion': '0.247%', 'gl': '0.218%', 'ben': '0.2%', 'aiz': '0.199%',
                            'pbct': '0.196%', 'ivz': '0.174%'}
            self.ticker_string = 'xlf'
            self.is_real_etf = True

        elif ticker == 'xlu':  # Hardcoded more than top 25 XLU (Utilities) holdings
            self.weights = {'nee': '15.297%', 'duk': '8.344%', 'so': '7.551%', 'd': '6.751%', 'aep': '4.674%',
                            'sre': '4.502%', 'exc': '4.408%', 'xel': '3.85%', 'peg': '3.491%', 'ed': '3.166%',
                            'es': '3.115%', 'wec': '3.106%', 'awk': '2.942%', 'eix': '2.4%', 'dte': '2.393%',
                            'fe': '2.386%', 'aee': '2.333%', 'etr': '2.315%', 'ppl': '2.293%', 'cms': '1.927%',
                            'cnp': '1.821%', 'ceg': '1.799%', 'evrg': '1.553%', 'lnt': '1.542%', 'aes': '1.493%',
                            'ato': '1.455%', 'ni': '1.202%', 'nrg': '0.993%', 'pnw': '0.82%'}
            self.ticker_string = 'xlu'
            self.is_real_etf = True

        elif ticker == 'xly':  # Hardcoded more than top 25 XLY (Consumer Discretionary) holdings
            self.weights = {'amzn': '21.148%', 'tsla': '17.826%', 'mcd': '5.316%', 'nke': '4.566%', 'hd': '4.507%',
                            'low': '4.425%', 'sbux': '3.09%', 'tgt': '2.842%', 'bkng': '2.734%', 'tjx': '2.292%',
                            'f': '2.132%', 'gm': '2.106%', 'dg': '1.308%', 'orly': '1.215%', 'mar': '1.21%',
                            'azo': '1.163%', 'cmg': '1.112%', 'hlt': '1.097%', 'yum': '1.004%', 'ebay': '0.978%',
                            'aptv': '0.974%', 'rost': '0.915%', 'dltr': '0.81%', 'dhi': '0.785%', 'expe': '0.732%',
                            'len': '0.706%', 'tsco': '0.682%', 'bby': '0.587%', 'vfc': '0.567%', 'ulta': '0.541%',
                            'grmn': '0.519%', 'gpc': '0.515%', 'pool': '0.501%', 'dri': '0.491%', 'rcl': '0.486%',
                            'nvr': '0.486%', 'kmx': '0.471%', 'mgm': '0.457%', 'ccl': '0.447%', 'czr': '0.446%',
                            'dpz': '0.443%', 'etsy': '0.44%', 'lvs': '0.412%', 'lkq': '0.408%', 'bbwi': '0.402%',
                            'aap': '0.4%', 'phm': '0.365%', 'whr': '0.341%', 'has': '0.332%', 'tpr': '0.29%',
                            'bwa': '0.289%', 'wynn': '0.242%', 'nwl': '0.241%', 'mhk': '0.231%', 'nclh': '0.207%',
                            'penn': '0.206%', 'pvh': '0.185%', 'rl': '0.155%', 'uaa': '0.098%', 'ua': '0.095%'}
            self.ticker_string = 'xly'
            self.is_real_etf = True

        elif ticker == 'soxx':  # Hardcoded more than top 25 SOXX (Semiconductors) holdings
            self.weights = {'avgo': '9.33%', 'qcom': '8.82%', 'nvda': '6.52%', 'intc': '6.26%', 'amd': '4.84%',
                            'mu': '4.34%', 'mrvl': '4.29%', 'tsm': '4.28%', 'amat': '4.12%', 'klac': '4.07%',
                            'txn': '4.06%', 'adi': '4.0%', 'nxpi': '3.95%', 'xlnx': '3.95%', 'lrcx': '3.85%',
                            'mchp': '3.77%', 'asml': '3.42%', 'on': '2.23%', 'swks': '2.14%', 'ter': '1.7%',
                            'mpwr': '1.6%', 'entg': '1.59%', 'qrvo': '1.32%', 'stm': '1.24%', 'wolf': '0.97%',
                            'mksi': '0.77%', 'umc': '0.73%', 'lscc': '0.69%', 'oled': '0.57%', 'asx': '0.47%'}
            self.ticker_string = 'soxx'
            self.is_real_etf = True

        elif ticker == 'xbi':  # Hardcoded more than top 25 XBI (Biotech) holdings
            self.weights = {'arna': '1.784%', 'bhvn': '1.266%', 'bcrx': '1.242%', 'vrtx': '1.133%', 'abbv': '1.085%',
                            'incy': '1.081%', 'ebs': '1.078%', 'alks': '1.063%', 'exel': '1.043%', 'amgn': '1.028%',
                            'ptct': '1.02%', 'ions': '1.02%', 'uthr': '1.02%', 'sage': '1.017%', 'acad': '1.005%',
                            'bmrn': '1.0%', 'irwd': '0.985%', 'nbix': '0.966%', 'halo': '0.962%', 'gbt': '0.956%',
                            'agio': '0.945%', 'apls': '0.931%', 'sgen': '0.916%', 'exas': '0.916%', 'biib': '0.916%',
                            'isee': '0.904%', 'cdna': '0.903%', 'gild': '0.901%', 'dvax': '0.898%', 'regn': '0.896%',
                            'hznp': '0.881%', 'ptgx': '0.881%', 'cytk': '0.86%', 'tptx': '0.857%', 'mrtx': '0.846%',
                            'rare': '0.84%', 'fold': '0.833%', 'iova': '0.831%', 'hrtx': '0.825%', 'tvtx': '0.814%',
                            'cldx': '0.804%', 'lgnd': '0.803%', 'ntla': '0.802%', 'mygn': '0.798%', 'insm': '0.795%',
                            'alny': '0.794%', 'vcel': '0.792%', 'dcph': '0.791%', 'beam': '0.791%', 'srpt': '0.786%',
                            'krtx': '0.784%', 'ccxi': '0.784%', 'bpmc': '0.761%', 'dnli': '0.754%', 'fate': '0.745%',
                            'vir': '0.743%', 'blue': '0.74%', 'ntra': '0.739%', 'swtx': '0.728%', 'vxrt': '0.728%',
                            'kod': '0.725%', 'prta': '0.717%', 'fgen': '0.716%', 'rlay': '0.716%', 'agen': '0.715%',
                            'twst': '0.71%', 'icpt': '0.708%', 'kymr': '0.691%', 'verv': '0.691%', 'atra': '0.685%',
                            'vcyt': '0.684%', 'rcus': '0.679%', 'arwr': '0.676%', 'zntl': '0.659%', 'arct': '0.656%',
                            'cere': '0.65%', 'nvta': '0.633%', 'kpti': '0.631%', 'ocgn': '0.629%', 'cdmo': '0.628%',
                            'mrna': '0.617%', 'rvmd': '0.609%', 'gthx': '0.601%', 'edit': '0.599%', 'tgtx': '0.592%',
                            'rxrx': '0.578%', 'myov': '0.576%', 'ino': '0.575%', 'allo': '0.569%', 'rgnx': '0.528%',
                            'mnkd': '0.525%', 'tsvt': '0.518%', 'enta': '0.515%', 'nvax': '0.514%', 'dmtk': '0.504%',
                            'opk': '0.503%', 'alt': '0.497%', 'orgo': '0.497%', 'alec': '0.493%', 'srne': '0.481%',
                            'kura': '0.473%', 'avxl': '0.456%', 'qure': '0.452%', 'mcrb': '0.45%', 'ibrx': '0.448%',
                            'mdgl': '0.443%', 'sndx': '0.44%', 'clvs': '0.428%', 'rckt': '0.425%', 'rdus': '0.42%',
                            'morf': '0.401%', 'chrs': '0.396%', 'imgn': '0.39%', 'cccc': '0.39%', 'xncr': '0.372%',
                            'sgmo': '0.362%', 'vnda': '0.35%', 'mgnx': '0.347%', 'albo': '0.34%', 'krys': '0.33%',
                            'cris': '0.326%', 'pmvp': '0.322%', 'idya': '0.304%', 'rapt': '0.301%', 'nrix': '0.294%',
                            'kros': '0.293%', 'goss': '0.287%', 'btai': '0.277%', 'sana': '0.276%', 'alxo': '0.268%',
                            'egrx': '0.264%', 'bbio': '0.262%', 'grts': '0.254%', 'itos': '0.253%', 'akba': '0.241%',
                            'anab': '0.239%', 'cvm': '0.238%', 'cprx': '0.237%', 'fmtx': '0.23%', 'repl': '0.229%',
                            'cmrx': '0.226%', 'vbiv': '0.225%', 'mrsn': '0.219%', 'rigl': '0.217%', 'fdmt': '0.212%',
                            'srrk': '0.211%', 'imvt': '0.21%'}
            self.ticker_string = 'xbi'
            self.is_real_etf = True

        # Set weights and ticker_string if not set
        if self.ticker_string is None:  # Actual ETF name was provided
            self.is_real_etf = True
            self.fill_holdings_from_marketwatch(ticker)
            self.ticker_string = ' '.join(list(self.weights.keys()))
        elif self.weights is None:
            self.weights = {ticker: '1.00%' for ticker in self.ticker_string.split(' ')}

        # Set ticker
        self.ticker = ticker

        # Set components
        self.set_components()

        # Query Finviz metrics for real ETFs
        if self.is_real_etf:
            finviz_fundamentals = get_finviz_metrics(ticker, ['Company', 'Dividend %', 'Price', 'SMA20', 'SMA50', 'SMA200', '52W High', 'Perf Year'])

            self.name = finviz_fundamentals['Company']
            self.dividend_yield = finviz_fundamentals['Dividend %']
            self.price = finviz_fundamentals['Price']
            self.sma20 = finviz_fundamentals['SMA20']
            self.sma50 = finviz_fundamentals['SMA50']
            self.sma200 = finviz_fundamentals['SMA200']
            self.high_52W = finviz_fundamentals['52W High']
            self.perf_year = finviz_fundamentals['Perf Year']

        # Calculate additional metrics based on components and weights

        # Weighted Median EV/GP
        relative_EV_to_GPs = []
        for ticker in self.weights.keys():
            try:
                for i in range(int(to_number(self.weights[ticker]) * 300)):
                    if self.components[ticker].ev_to_gp_ratio is not None:
                        relative_EV_to_GPs.append(self.components[ticker].ev_to_gp_ratio)
            except Exception as e:
                pass
        try:
            self.weighted_median_EV_to_GP = get_median_from_list(relative_EV_to_GPs)
        except Exception as e:
            self.weighted_median_EV_to_GP = None

        # Weighted Median EV/EBIT
        relative_EV_to_EBITs = []
        for ticker in self.weights.keys():
            try:
                for i in range(int(to_number(self.weights[ticker]) * 300)):
                    if self.components[ticker].ev_to_ebit_ratio is not None:
                        if to_number(self.components[ticker].ev_to_ebit_ratio) > 0:
                            relative_EV_to_EBITs.append(self.components[ticker].ev_to_ebit_ratio)
                        else:
                            relative_EV_to_EBITs.append(1000000)
            except Exception as e:
                pass
        try:
            self.weighted_median_EV_to_EBIT = get_median_from_list(relative_EV_to_EBITs)
        except Exception as e:
            self.weighted_median_EV_to_EBIT = None

        # Weighted Median Adj. EV/EBIT
        relative_adj_EV_to_EBITs = []
        for ticker in self.weights.keys():
            try:
                for i in range(int(to_number(self.weights[ticker]) * 300)):
                    if self.components[ticker].adj_ev_to_ebit_ratio is not None:
                        if to_number(self.components[ticker].adj_ev_to_ebit_ratio) > 0:
                            relative_adj_EV_to_EBITs.append(self.components[ticker].adj_ev_to_ebit_ratio)
                        else:
                            relative_adj_EV_to_EBITs.append(1000000)
            except Exception as e:
                pass
        try:
            self.weighted_median_adj_EV_to_EBIT = get_median_from_list(relative_adj_EV_to_EBITs)
        except Exception as e:
            self.weighted_median_adj_EV_to_EBIT = None

        # Weighted Median "Median Revenue Growth 3Y"
        relative_med_rev_growth = []
        for ticker in self.weights.keys():
            try:
                for i in range(int(to_number(self.weights[ticker]) * 300)):
                    if self.components[ticker].med_rev_growth_3y is not None:
                        relative_med_rev_growth.append(self.components[ticker].med_rev_growth_3y)
            except Exception as e:
                pass
        try:
            self.weighted_med_med_rev_growth_3y = get_median_from_list(relative_med_rev_growth)
        except Exception as e:
            self.weighted_med_med_rev_growth_3y = None

        # Weighted Median Gross Margin
        relative_med_gross_margin = []
        for ticker in self.weights.keys():
            try:
                for i in range(int(to_number(self.weights[ticker]) * 300)):
                    if self.components[ticker].gross_margin is not None:
                        relative_med_gross_margin.append(self.components[ticker].gross_margin)
            except Exception as e:
                pass
        try:
            self.weighted_med_gross_margin = get_median_from_list(relative_med_gross_margin)
        except Exception as e:
            self.weighted_med_gross_margin = None

        # Weighted Median Adj EBIT Margin
        relative_med_adj_ebit_margin = []
        for ticker in self.weights.keys():
            try:
                for i in range(int(to_number(self.weights[ticker]) * 300)):
                    if self.components[ticker].adj_ebit_margin is not None:
                        relative_med_adj_ebit_margin.append(self.components[ticker].adj_ebit_margin)
            except Exception as e:
                pass
        try:
            self.weighted_med_adj_ebit_margin = get_median_from_list(relative_med_adj_ebit_margin)
        except Exception as e:
            self.weighted_med_adj_ebit_margin = None

        # Weighted Median EBIT Margin (not adjusted)
        relative_med_ebit_margin = []
        for ticker in self.weights.keys():
            try:
                for i in range(int(to_number(self.weights[ticker]) * 300)):
                    if self.components[ticker].ebit_margin is not None:
                        relative_med_ebit_margin.append(self.components[ticker].ebit_margin)
            except Exception as e:
                pass
        try:
            self.weighted_med_ebit_margin = get_median_from_list(relative_med_ebit_margin)
        except Exception as e:
            self.weighted_med_ebit_margin = None

        # Weighted % holdings within 5% of 52W High
        numer = 0
        denom = 0

        for ticker in self.weights.keys():
            try:
                if self.components[ticker].high_52W is not None:
                    if to_number(self.components[ticker].high_52W) >= -0.05:
                        numer += to_number(self.weights[ticker])
                    denom += to_number(self.weights[ticker])
            except Exception as e:
                pass
        if denom == 0:
            self.percent_at_high = to_percent_string(0)
        else:
            self.percent_at_high = to_percent_string(numer / denom)

        # Weighted % holdings within 5% of 52W Low
        numer = 0
        denom = 0

        for ticker in self.weights.keys():
            try:
                if self.components[ticker].low_52W is not None:
                    if to_number(self.components[ticker].low_52W) <= 0.05:
                        numer += to_number(self.weights[ticker])
                    denom += to_number(self.weights[ticker])
            except Exception as e:
                pass
        if denom == 0:
            self.percent_at_low = to_percent_string(0)
        else:
            self.percent_at_low = to_percent_string(numer / denom)

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
                if 'USD' in ticker and ticker != 'USD':
                    self.components[ticker] = Crypto(ticker)
                else:
                    self.components[ticker] = Stock(ticker)
                    if self.components[ticker].type == 'ETF':
                        self.components[ticker] = ETF(ticker)
            except Exception as e:
                pass

    # For each stock in an ETF, displays data selected in columns
    def display_metrics(self, columns, only_nums=False, extra_header=False, include_overall=False):
        header = ''
        for metric_title in columns:
            header += metric_title + '\t'
        if extra_header:
            header += '=IF(C1="Stock", E1, IFERROR(0/0))\t=IF(C1="ETF", E1, IFERROR(0/0))\t=IF(C1="Stock", F1, IFERROR(0/0))\t=IF(C1="ETF", F1, IFERROR(0/0))\t'
        print(header)

        tickers = sorted(list(self.components.keys()))

        if include_overall:
            tickers.insert(0, self.ticker)

        for i, ticker in enumerate(tickers):
            try:
                if include_overall and i == 0:
                    component = self
                else:
                    component = self.components[ticker]  # Either a stock, a crypto, or an ETF

                line = ''

                for metric_title in columns:
                    try:
                        if metric_title == 'Ticker':  # Works for both stocks and ETFs
                            line += component.ticker + '\t'
                        if metric_title == 'Name':  # Works for both stocks and ETFs
                            line += component.name + '\t'
                        if metric_title == 'Type':  # Works for both stocks and ETFs
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
                            if component.type == 'Stock':
                                line += component.ev_to_gp_ratio + '\t'
                            else:
                                line += component.weighted_median_EV_to_GP + '\t'
                        if metric_title == 'EV/EBITDA':
                            line += component.ev_to_ebitda_ratio + '\t'
                        if metric_title == 'EV/EBIT':
                            if component.type == 'Stock':
                                line += component.ev_to_ebit_ratio + '\t'
                            else:
                                line += component.weighted_median_EV_to_EBIT + '\t'
                        if metric_title == 'Adj EV/EBIT':
                            if component.type == 'Stock':
                                line += component.adj_ev_to_ebit_ratio + '\t'
                            else:
                                line += component.weighted_median_adj_EV_to_EBIT + '\t'

                        if metric_title == 'Sales Growth 3Y':
                            line += component.revenue_growth_3y + '\t'
                        if metric_title == 'Median Rev Growth 3Y':
                            if component.type == 'Stock':
                                line += component.med_rev_growth_3y + '\t'
                            else:
                                line += component.weighted_med_med_rev_growth_3y + '\t'
                        if metric_title == 'Median Rev Growth':
                            line += component.med_rev_growth + '\t'

                        if metric_title == 'Gross Margin':
                            if component.type == 'Stock':
                                line += component.gross_margin + '\t'
                            else:
                                line += component.weighted_med_gross_margin + '\t'
                        if metric_title == 'EBITDA Margin':
                            line += component.ebitda_margin + '\t'
                        if metric_title == 'Adj EBIT Margin':
                            if component.type == 'Stock':
                                line += component.adj_ebit_margin + '\t'
                            else:
                                line += component.weighted_med_adj_ebit_margin + '\t'
                        if metric_title == 'EBIT Margin':
                            if component.type == 'Stock':
                                line += component.ebit_margin + '\t'
                            else:
                                line += component.weighted_med_ebit_margin + '\t'
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

                        if metric_title == '52W High':  # Works for both stocks and ETFs
                            line += component.high_52W + '\t'
                        if metric_title == 'Perf Year':
                            line += component.perf_year + '\t'
                        if metric_title == 'SMA20':
                            line += component.sma20 + '\t'
                        if metric_title == 'SMA50':
                            line += component.sma50 + '\t'
                        if metric_title == 'SMA200':
                            line += component.sma200 + '\t'

                        # ETF Only Metrics
                        if metric_title == 'Weighted Median EV/GP':
                            line += component.weighted_median_EV_to_GP + '\t'
                        if metric_title == 'Weighted Median EV/EBIT':
                            line += component.weighted_median_EV_to_EBIT + '\t'
                        if metric_title == 'Weighted Median Adj EV/EBIT':
                            line += component.weighted_median_adj_EV_to_EBIT + '\t'
                        if metric_title == 'Weighted Median Median Rev Growth 3Y':
                            line += component.weighted_med_med_rev_growth_3y + '\t'
                        if metric_title == 'Weighted Median Gross Margin':
                            line += component.weighted_med_gross_margin + '\t'
                        if metric_title == 'Weighted Median Adj EBIT Margin':
                            line += component.weighted_med_adj_ebit_margin + '\t'

                        if metric_title == '% at 52W High':
                            line += component.percent_at_high + '\t'
                        if metric_title == '% at 52W Low':
                            line += component.percent_at_low + '\t'

                    except Exception as e:
                        line += '' + '\t'

                if only_nums:
                    line = ''.join(x for i, x in enumerate(line) if i-1 < 0 or x not in 'BMK' or line[i-1] not in '1234567890')
                print(line)

            except OverflowError:
                pass
            except Exception as e:
                pass
