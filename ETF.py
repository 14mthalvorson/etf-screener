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
        self.leverage = None
        self.expense_ratio = None

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
                                 'ba baba bac bam band bill bkng bl blk bmo bmy bns bp bti bud bulz ' \
                                 'c cat cb cci cdns chgg chtr ci clou cmcsa cme cni coin cop cost coup cour ' \
                                 'cpng crm crwd csco csx cvna cvs cvx cybr ddog de deo dhr dis dlr docu domo dpz ' \
                                 'dsgx dt duk edv eght el enb eqix eqnr estc etsy evbg f fb fivn fngg fngs ' \
                                 'frog fvrr ge gild glob gm googl gs gsk gtlb hd hdb hon hood hsbc hubs ibb ibm ' \
                                 'ibn infy intc intu irm isrg itb iye iyr jamf jd jnj jpm ko lin lly lmnd ' \
                                 'lmt logi low lrcx ltpz ma mcd mdb mdlz mdt meli metv mime mmc mmm mo moat morn mrk ' \
                                 'mrna mrvl ms msft mtch mttr mu nee net newr nflx nke now nvda nvo nvs o oih ' \
                                 'okta open orcl panw path payc pbr pd pdd pdi pep pfe pg pins plan pld pltr pm pnc ' \
                                 'pton pypl qcom qqq qtwo rblx rdfn rng roku rpd rtx ry sap sbac sbux ' \
                                 'schw se shop shw sklz smar smh snap snow sny sofi sony soxx spgi splk spot spy sq ' \
                                 'sumo syk t td tdoc team tenb ter tfc tgt tjx tm tmf tmo tmus tsla tsm ' \
                                 'ttd tte ttwo twlo twtr txn tyd tyl u ul unh unp ups upst upwk usb v vale ' \
                                 'veev vig vmw vnq vpn vpu vrsn vtv vug vz wcld wday we wfc wix wm wmt w ' \
                                 'xbi xhb xlb xle xlf xli xlk xlp xlu xlc xlv xly xme xom xop xrt xtl zen zg zm zs zts'

        elif ticker == 'mine':  # My Holdings
            self.ticker_string = 'aapl abnb abt adbe adsk ai akam amd amt amzn anet anss api appf appn apps arkf ' \
                                 'arkg arkk arkw asan avgo avlr awk axp band bill bl bmy bulz cci cdns chgg clou ' \
                                 'cmcsa coin cost coup cour cpng crm crwd csco cvna cybr ddog dis dlr docu domo dpz ' \
                                 'dsgx dt edv eght eqix estc etsy evbg fb fivn fngg fngo frog fvrr glob googl ' \
                                 'gtlb hood hubs ibb idna irm jamf lmnd logi ltpz ma mdb meli metv mime morn ' \
                                 'mrna mrvl msft mtch mttr mu net newr nflx now nvda o okta open panw path payc pd ' \
                                 'pdi pins plan pltr pton pypl qcom qld qqq qtwo rblx rdfn rng roku rom rpd sbac se ' \
                                 'shop sklz smar snap snow sofi soxx spgi splk spot sq sumo tdoc team tenb ter tmf ' \
                                 'tqqq tsla tsm ttd ttwo twlo twtr tyd tyl u upro upwk usd v veev vig vmw vpn vpu ' \
                                 'vrsn wcld wday we wix wm xbi z zen zg zm zs'

        elif ticker == 'my_top':  # My Top Holdings
            self.ticker_string = 'googl amzn tmf fb coin msft crm shop crwd ttd aapl se adbe nvda ddog ' \
                                 'veev sq pltr net now hubs fngg fngu bulz twlo etsy pins tdoc qqq'

        elif ticker == 'market_cap':  # GP relevant companies
            self.ticker_string = 'aapl msft googl amzn tsla fb tsm nvda v jnj jpm unh wmt pg bac hd baba ma tm xom pfe ' \
                            'asml dis ko cvx adbe csco abbv pep nke cmcsa lly tmo avgo acn orcl vz wfc abt crm cost nvs ' \
                            'nflx intc mrk pypl dhr t qcom mcd azn ms ups nvo schw bbl sap lin ry txn pm unp low ' \
                            'tte intu nee td hsbc sony hon bmy mdt axp amd cvs rtx ul tmus sny shop c amgn blk ' \
                            'ba ibm amat cop jd cat deo gs amt bud de sbux pld gsk hdb antm lmt el bp tgt isrg ' \
                            'ge chtr mmm now bkng infy bti eqnr spgi syk mu zts adp mdlz mo abnb pnc se usb bns cni ' \
                            'bam tfc gild enb lrcx cb f pbr adi snow tjx cme vale mmc ci pdd cci shw duk csx ' \
                            'gm bmo ibn'

        elif ticker == 'revenue':  # GP relevant companies
            self.ticker_string = 'wmt amzn aapl unh cvs tm xom googl cost msft t ci tte hd jd cvx f vz antm bp gm ' \
                            'cmcssa fb tgt low ups jnj sony tmus intc pg pep ge ibm bam pfe eqnr dis lmt gs rtx ba ' \
                            'ms jpm tsm ul vale abbv acn bud nvs chtr csco c cat mrk bac tsla nke tjx bmy'

        elif ticker == 'top_ETFs':  # Popular ETFs
            self.ticker_string = 'spy qqq vtv vug vig arkk moat vpn wcld soxx xlv xlu xlf'

        elif ticker == 'vanguard':  # Vanguard ETFs
            self.ticker_string = 'vig esgv vug vym vv mgc mgk mgv vone vong vonv vthr voo voog voov vti vtv vxf ' \
                                 'vo vot voe ivoo ivog ivov vtwo vtwg vtwv vioo viog viov vb vbk vbr vt'

        elif ticker == 'high_returns':  # BULZ ETF Holdings
            self.ticker_string = 'xlk soxx smh qqq spy xlv arkw tan qcln arkk xlf lit ixn pbw pall'

        elif ticker == 'my_ETFs':  # Popular ETFs
            self.ticker_string = 'spy qqq vtv vug vig arkk moat vpn wcld soxx xlv vpu xlf vpu metv ibb clou xbi arkw arkf arkg'

        elif ticker == 'sector_ETFs':  # Sector ETFs
            self.ticker_string = 'spy qqq vtv vig vpn soxx xle xlf xlu xli xlk xlv xly xlp xlb xlc xop iyr xhb itb vnq iye oih xme xrt smh ibb xtl'

        elif ticker == 'LETFs':  # Leveraged ETFs
            self.ticker_string = 'qqq qld tqqq spy sso upro xlk tecl fngs fngo fngu bulz rom fngg vpn'

        elif ticker == 'mega':  # Mega-cap tech stocks
            self.ticker_string = 'aapl amzn googl fb nflx nvda tsla msft tsm'

        elif ticker == 'reit':  # Digital REIT stocks
            self.ticker_string = 'sbac dlr eqix amt acc o cci irm'

        elif ticker == 'fngg':  # FNGG ETF Holdings
            self.ticker_string = 'googl amd fb nvda amzn msft aapl nflx rblx zs snap crwd se ddog nio snow u tsla zm shop'
            self.is_real_etf = True
            self.leverage = '2x'
            self.expense_ratio = '1.09%'

        elif ticker == 'fngs' or ticker == 'fngo' or ticker == 'fngu':  # FNGU ETF Holdings
            self.ticker_string = 'amzn aapl googl fb tsla twtr nvda nflx baba bidu'
            self.is_real_etf = True
            if ticker == 'fngs':
                self.leverage = '1x'
                self.expense_ratio = '0.57%'
            if ticker == 'fngo':
                self.leverage = '2x'
                self.expense_ratio = '0.95%'
            elif ticker == 'fngu':
                self.leverage = '3x'
                self.expense_ratio = '0.95%'

        elif ticker == 'bulz':  # BULZ ETF Holdings
            self.ticker_string = 'aapl amd amzn crm fb googl intc msft mu nflx nvda pypl qcom sq tsla'
            self.is_real_etf = True
            self.expense_ratio = '0.95%'
            self.leverage = '3x'

        elif ticker == 'crypto':  # Cryptocurrencies
            self.ticker_string = 'BTCUSD ETHUSD XRPUSD LTCUSD'

        elif ticker == 'qqq' or ticker == 'qld' or ticker == 'tqqq':  # Hardcoded more than top 25 QQQ holdings
            self.weights = {'aapl': '12.738%', 'msft': '10.156%', 'amzn': '6.324%', 'googl': '7.936%', 'tsla': '4.019%',
                            'nvda': '3.783%', 'fb': '3.783%', 'adbe': '1.811%', 'pep': '1.806%',
                            'avgo': '1.781%', 'csco': '1.734%', 'cost': '1.717%', 'cmcsa': '1.686%', 'qcom': '1.494%',
                            'intc': '1.463%', 'nflx': '1.338%', 'txn': '1.208%', 'intu': '1.13%', 'tmus': '1.124%',
                            'pypl': '1.088%', 'amd': '1.08%', 'hon': '0.983%', 'amgn': '0.94%', 'amat': '0.918%',
                            'sbux': '0.839%', 'chtr': '0.815%', 'isrg': '0.76%', 'bkng': '0.746%', 'mdlz': '0.706%',
                            'mu': '0.683%', 'adi': '0.649%', 'adp': '0.644%', 'lrcx': '0.618%', 'gild': '0.611%',
                            'csx': '0.572%', 'fisv': '0.523%', 'mrna': '0.495%', 'regn': '0.489%', 'vrtx': '0.462%',
                            'atvi': '0.458%', 'klac': '0.422%', 'mrvl': '0.421%', 'ilmn': '0.415%', 'kdp': '0.409%',
                            'jd': '0.397%', 'mar': '0.393%', 'nxpi': '0.393%', 'asml': '0.39%', 'adsk': '0.389%',
                            'abnb': '0.386%', 'meli': '0.376%', 'xlnx': '0.375%', 'panw': '0.362%', 'ftnt': '0.362%',
                            'snps': '0.345%', 'idxx': '0.34%', 'mnst': '0.339%', 'aep': '0.468%', 'ctsh': '0.337%',
                            'wday': '0.335%', 'orly': '0.332%', 'lcid': '0.331%', 'khc': '0.327%', 'payx': '0.319%',
                            'wba': '0.319%', 'exc': '0.319%', 'team': '0.318%', 'lulu': '0.307%', 'mchp': '0.307%',
                            'cdns': '0.302%', 'dxcm': '0.302%', 'ctas': '0.297%', 'algn': '0.296%', 'ea': '0.289%',
                            'odfl': '0.281%', 'bidu': '0.279%', 'xel': '0.279%', 'ebay': '0.267%', 'ddog': '0.264%',
                            'crwd': '0.262%', 'zs': '0.256%', 'rost': '0.25%', 'zm': '0.249%', 'pcar': '0.245%',
                            'fast': '0.242%', 'biib': '0.241%', 'vrsk': '0.236%', 'mtch': '0.236%', 'cprt': '0.227%',
                            'dltr': '0.221%', 'ntes': '0.211%', 'anss': '0.211%', 'okta': '0.201%', 'siri': '0.199%',
                            'sgen': '0.184%', 'vrsn': '0.181%', 'pdd': '0.171%', 'swks': '0.171%', 'docu': '0.167%',
                            'splk': '0.138%'}
            self.ticker_string = ticker
            self.is_real_etf = True

        elif ticker == 'schg':  # Hardcoded Schwab Large Cap Growth
            self.weights = {'aapl': '14.24%', 'msft': '12.05%', 'googl': '8.54%', 'amzn': '7.36%', 'tsla': '3.91%',
                            'nvda': '3.43%', 'fb': '2.86%', 'unh': '2.43%', 'v': '2.01%', 'ma': '1.72%',
                            'avgo': '1.29%', 'adbe': '1.25%', 'cost': '1.22%', 'tmo': '1.21%', 'crm': '1.13%',
                            'nflx': '0.96%', 'dhr': '0.95%', 'lin': '0.84%', 'intu': '0.84%', 'amd': '0.81%',
                            'pypl': '0.74%', 'now': '0.65%', 'blk': '0.59%', 'amt': '0.59%', 'bkng': '0.57%',
                            'isrg': '0.55%', 'spgi': '0.51%', 'zts': '0.50%', 'lrcx': '0.44%', 'ci': '0.41%',
                            'chtr': '0.40%', 'tmus': '0.39%', 'el': '0.39%', 'snow': '0.38%', 'ew': '0.37%',
                            'shw': '0.36%', 'regn': '0.35%', 'uber': '0.33%', 'bsx': '0.33%', 'eqix': '0.33%',
                            'vrtx': '0.32%', 'abnb': '0.32%', 'fisv': '0.31%', 'mco': '0.30%', 'ilmn': '0.30%',
                            'hum': '0.29%', 'sq': '0.29%', 'nxpi': '0.28%', 'adsk': '0.28%', 'panw': '0.27%',
                            'cnc': '0.26%', 'nem': '0.26%', 'iqv': '0.25%', 'snps': '0.25%', 'dg': '0.25%',
                            'rop': '0.25%', 'wday': '0.24%', 'msci': '0.24%', 'ddog': '0.24%', 'idxx': '0.24%',
                            'cmg': '0.24%', 'orly': '0.24%', 'ftnt': '0.23%', 'snap': '0.23%', 'hlt': '0.23%',
                            'dxcm': '0.23%', 'gpn': '0.22%', 'lhx': '0.22%', 'mck': '0.22%', 'cdns': '0.22%',
                            'azo': '0.22%', 'lulu': '0.21%', 'algn': '0.21%', 'crwd': '0.21%', 'kkr': '0.21%',
                            'sivb': '0.20%', 'ttd': '0.19%', 'rmd': '0.19%', 'mtd': '0.19%', 'cbre': '0.19%',
                            'twlo': '0.18%', 'sbac': '0.18%', 'tdg': '0.18%', 'ctas': '0.18%', 'veev': '0.17%',
                            'net': '0.17%', 'zm': '0.17%', 'mnst': '0.17%', 'vrsk': '0.17%', 'mdb': '0.16%',
                            'twtr': '0.16%', 'wst': '0.16%', 'anss': '0.15%', 'hal': '0.15%', 'okta': '0.15%',
                            'expe': '0.15%', 'odfl': '0.15%', 'anet': '0.15%', 'csgp': '0.15%', 'cprt': '0.15%',
                            'lng': '0.14%', 'on': '0.14%', 'vmw': '0.14%', 'epam': '0.14%', 'docu': '0.13%',
                            'zbra': '0.13%', 'hubs': '0.13%', 'it': '0.13%', 'bkr': '0.13%', 'uri': '0.13%',
                            'pki': '0.12%', 'bill': '0.12%', 'avtr': '0.12%', 'zs': '0.12%', 'fang': '0.12%',
                            'hznp': '0.12%', 'lbrdk': '0.12%', 'enph': '0.11%', 'ulta': '0.11%', 'flt': '0.11%',
                            'ttwo': '0.11%', 'coo': '0.11%', 'tdy': '0.11%', 'tyl': '0.11%', 'roku': '0.10%',
                            'splk': '0.10%', 'czr': '0.10%', 'pool': '0.10%', 'gnrc': '0.10%', 'etsy': '0.10%',
                            'u': '0.10%', 'alny': '0.10%', 'moh': '0.10%', 'ssnc': '0.09%', 'dell': '0.09%',
                            'mpwr': '0.09%', 'payc': '0.09%', 'podd': '0.09%', 'crl': '0.09%', 'mkl': '0.09%',
                            'nvr': '0.09%', 'bmrn': '0.09%', 'sgen': '0.09%', 'tech': '0.09%', 'lyv': '0.09%',
                            'dpz': '0.08%', 'dash': '0.08%', 'fds': '0.08%', 'tfx': '0.08%', 'qrvo': '0.08%',
                            'pins': '0.08%', 'rng': '0.08%', 'fico': '0.08%', 'foxa': '0.07%', 'mktx': '0.07%',
                            'exas': '0.07%', 'abmd': '0.07%', 'zen': '0.07%', 'sedg': '0.07%', 'bio': '0.07%',
                            'cvna': '0.07%', 'incy': '0.07%', 'ptc': '0.07%', 'ndsn': '0.07%', 'lyft': '0.07%',
                            'gddy': '0.07%', 'masi': '0.06%', 'tdoc': '0.06%', 'w': '0.06%', 'plug': '0.06%',
                            'fnd': '0.06%', 'pton': '0.06%', 'cien': '0.05%', 'coup': '0.05%', 'rgen': '0.05%',
                            'trex': '0.05%', 'avlr': '0.05%', 'five': '0.05%', 'path': '0.05%', 'synh': '0.05%',
                            'axon': '0.05%', 'y': '0.05%', 'fivn': '0.05%', 'dt': '0.05%', 'cnxc': '0.05%',
                            'txg': '0.05%', 'afrm': '0.05%', 'deck': '0.04%', 'pcty': '0.04%', 'z': '0.04%',
                            'pen': '0.04%', 'sofi': '0.04%', 'cabo': '0.04%', 'dkng': '0.04%', 'wex': '0.04%',
                            'nbix': '0.04%'}
            self.ticker_string = ticker
            self.is_real_etf = True

        elif ticker == 'spy' or ticker == 'sso' or ticker == 'upro' or ticker == 'voo':  # Hardcoded more than top 25 SPY holdings
            self.weights = {'aapl': '7.107666%', 'msft': '5.965681%', 'amzn': '3.194360%', 'googl': '4.374%',
                            'tsla': '1.912091%', 'nvda': '1.579144%', 'fb': '1.483880%',
                            'unh': '1.214215%', 'jnj': '1.199590%', 'jpm': '1.159040%', 'pg': '1.048071%',
                            'v': '1.024148%', 'hd': '1.015449%', 'ma': '0.893443%', 'xom': '0.889748%',
                            'bac': '0.881877%', 'pfe': '0.790265%', 'cvx': '0.682994%', 'dis': '0.671143%',
                            'abbv': '0.656220%', 'adbe': '0.640114%', 'pep': '0.639565%', 'ko': '0.631725%',
                            'avgo': '0.630636%', 'tmo': '0.618314%', 'csco': '0.614070%', 'cost': '0.608044%',
                            'abt': '0.606727%', 'cmcsa': '0.598096%', 'vz': '0.587396%', 'wfc': '0.580134%',
                            'acn': '0.576389%', 'crm': '0.549432%', 'wmt': '0.530024%', 'qcom': '0.529059%',
                            'mrk': '0.526076%', 'intc': '0.517914%', 'mcd': '0.513691%', 'lly': '0.512679%',
                            'nke': '0.488689%', 'dhr': '0.486310%', 'nflx': '0.473847%', 't': '0.461224%',
                            'ups': '0.439826%', 'txn': '0.427726%', 'low': '0.427537%', 'pm': '0.425558%',
                            'lin': '0.421537%', 'unp': '0.414311%', 'intu': '0.399085%', 'nee': '0.392138%',
                            'ms': '0.387284%', 'pypl': '0.385207%', 'amd': '0.383152%', 'cvs': '0.377340%',
                            'bmy': '0.374470%', 'rtx': '0.367593%', 'mdt': '0.362671%', 'schw': '0.352483%',
                            'orcl': '0.348547%', 'hon': '0.348202%', 'c': '0.341520%', 'amgn': '0.334095%',
                            'ibm': '0.325135%', 'amat': '0.325093%', 'gs': '0.321312%', 'cop': '0.316099%',
                            'axp': '0.304517%', 'pld': '0.304174%', 'blk': '0.303070%', 'amt': '0.300105%',
                            'ba': '0.299357%', 'sbux': '0.297529%', 'now': '0.294392%', 'antm': '0.290040%',
                            'cat': '0.286188%', 'ge': '0.284134%', 'de': '0.276861%', 'tgt': '0.274456%',
                            'isrg': '0.267869%', 'bkng': '0.263558%', 'spgi': '0.262086%', 'lmt': '0.252863%',
                            'zts': '0.250739%', 'mmm': '0.250492%', 'mdlz': '0.250051%', 'mo': '0.244828%',
                            'mu': '0.243013%', 'cb': '0.235566%', 'pnc': '0.232757%', 'adi': '0.229474%',
                            'adp': '0.228519%', 'cme': '0.227966%', 'tfc': '0.222503%', 'tjx': '0.221781%',
                            'syk': '0.221604%', 'lrcx': '0.218617%', 'gild': '0.215861%', 'duk': '0.213562%',
                            'usb': '0.210119%', 'cci': '0.206757%', 'f': '0.205487%', 'bdx': '0.204622%',
                            'gm': '0.203000%', 'mmc': '0.202808%', 'csx': '0.202457%', 'chtr': '0.199148%',
                            'so': '0.193051%', 'ci': '0.190160%', 'ice': '0.189623%', 'tmus': '0.186520%',
                            'fis': '0.185389%', 'el': '0.185086%', 'cl': '0.183736%', 'ew': '0.183135%',
                            'shw': '0.182909%', 'itw': '0.182221%', 'nsc': '0.177027%', 'd': '0.172433%',
                            'eog': '0.171831%', 'regn': '0.171784%', 'pgr': '0.169011%', 'eqix': '0.168482%',
                            'fisv': '0.166785%', 'cof': '0.166444%', 'etn': '0.164603%', 'apd': '0.163719%',
                            'vrtx': '0.163437%', 'atvi': '0.161652%', 'aon': '0.160655%', 'fdx': '0.160304%',
                            'bsx': '0.159741%', 'mrna': '0.152555%', 'hca': '0.152120%', 'emr': '0.152027%',
                            'klac': '0.150331%', 'wm': '0.149393%', 'noc': '0.148128%', 'fcx': '0.147696%',
                            'psa': '0.147370%', 'ilmn': '0.147070%', 'mco': '0.145128%', 'hum': '0.144148%',
                            'slb': '0.142040%', 'nxpi': '0.138469%', 'adsk': '0.137735%', 'pxd': '0.133048%',
                            'xlnx': '0.132229%', 'aig': '0.130268%', 'nem': '0.130038%', 'met': '0.129223%',
                            'jci': '0.129184%', 'gd': '0.128951%', 'rop': '0.128095%', 'dg': '0.127325%',
                            'iqv': '0.126206%', 'spg': '0.125948%', 'tel': '0.125489%', 'cnc': '0.125154%',
                            'mpc': '0.124956%', 'aph': '0.124531%', 'ecl': '0.123997%', 'info': '0.122042%',
                            'snps': '0.121938%', 'bk': '0.121754%', 'kmb': '0.121022%', 'idxx': '0.120732%',
                            'dow': '0.120224%', 'ctsh': '0.119093%', 'aep': '0.118824%', 'orly': '0.117346%',
                            'msci': '0.117297%', 'mar': '0.116698%', 'hpq': '0.114642%', 'sre': '0.114577%',
                            'bax': '0.113305%', 'a': '0.113290%', 'pru': '0.113043%', 'exc': '0.112742%',
                            'trv': '0.112587%', 'azo': '0.112321%', 'adm': '0.111441%', 'gpn': '0.111414%',
                            'lhx': '0.110534%', 'gis': '0.110217%', 'dlr': '0.109325%', 'mck': '0.108911%',
                            'mchp': '0.108558%', 'dd': '0.107062%', 'cmg': '0.106869%', 'syy': '0.106705%',
                            'cdns': '0.106679%', 'dxcm': '0.106641%', 'ftnt': '0.106011%', 'ph': '0.105872%',
                            'hlt': '0.105773%', 'carr': '0.105638%', 'msi': '0.105047%', 'afl': '0.103188%',
                            'stz': '0.103030%', 'ea': '0.102879%', 'o': '0.102485%', 'tt': '0.101058%',
                            'psx': '0.100562%', 'payx': '0.100212%'}
            self.ticker_string = ticker
            self.is_real_etf = True

        elif ticker == 'voog':  # SP500 Growth
            self.weights = {'aapl': '13.01%', 'msft': '11.87%', 'amzn': '6.83%', 'googl': '7.90%', 'tsla': '4.04%',
                            'fb': '3.74%', 'nvda': '3.46%', 'hd': '1.56%', 'adbe': '1.27%', 'nflx': '1.25%',
                            'tmo': '1.24%', 'lly': '1.03%', 'jpm': '1.01%', 'qcom': '0.96%', 'unh': '0.93%',
                            'intu': '0.86%', 'low': '0.84%', 'pfe': '0.84%', 'amd': '0.74%', 'v': '0.73%',
                            'avgo': '0.73%', 'crm': '0.71%', 'acn': '0.71%', 'ma': '0.69%', 'dhr': '0.67%',
                            'amat': '0.67%', 'orcl': '0.66%', 'bac': '0.66%', 'abt': '0.62%', 'gs': '0.61%',
                            'abbv': '0.61%', 'now': '0.61%', 'cost': '0.60%', 'pypl': '0.56%', 'csco': '0.56%',
                            'nke': '0.54%', 'lrcx': '0.48%', 'pep': '0.47%', 'lin': '0.42%', 'mcd': '0.42%',
                            'mrna': '0.42%', 'isrg': '0.42%', 'schw': '0.40%', 'txn': '0.40%', 'zts': '0.36%',
                            'pld': '0.36%', 'sbux': '0.33%', 'spgi': '0.33%', 'ms': '0.32%', 'blk': '0.32%',
                            'amt': '0.32%', 'ups': '0.32%', 'regn': '0.31%', 'unp': '0.31%', 'klac': '0.31%',
                            'tgt': '0.29%', 'adp': '0.26%', 'mmc': '0.25%', 'dxcm': '0.24%'}
            self.ticker_string = 'voog'
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
            self.weights = {'unh': '2.58%', 'jpm': '2.55%', 'jnj': '2.45%', 'pg': '2.16%',
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

        elif ticker == 'xlk' or ticker == 'tecl':  # Hardcoded more than top 25 XLK (Technology) holdings
            self.weights = {'aapl': '24.886650%', 'msft': '21.017344%', 'nvda': '4.052700%', 'v': '3.682019%',
                            'ma': '3.153710%', 'avgo': '2.337783%', 'adbe': '2.331992%', 'csco': '2.248991%',
                            'acn': '2.099874%', 'crm': '2.053041%', 'qcom': '1.895380%', 'intc': '1.893916%',
                            'txn': '1.517018%', 'intu': '1.492442%', 'amd': '1.443475%', 'pypl': '1.378747%',
                            'orcl': '1.258661%', 'ibm': '1.189593%', 'amat': '1.188000%', 'now': '1.102448%',
                            'mu': '0.874357%', 'adp': '0.838943%', 'adi': '0.835345%', 'lrcx': '0.777534%',
                            'fis': '0.671553%', 'fisv': '0.608157%', 'klac': '0.550457%', 'adsk': '0.511012%',
                            'nxpi': '0.506153%', 'xlnx': '0.503456%', 'tel': '0.452170%', 'aph': '0.450666%',
                            'snps': '0.449788%', 'ctsh': '0.445428%', 'hpq': '0.417622%', 'gpn': '0.411868%',
                            'ftnt': '0.402946%', 'mchp': '0.394989%', 'cdns': '0.393005%', 'msi': '0.386228%',
                            'payx': '0.372127%', 'glw': '0.313283%', 'keys': '0.295693%', 'anss': '0.278080%',
                            'anet': '0.264886%', 'zbra': '0.257381%', 'cdw': '0.250944%', 'epam': '0.245540%',
                            'it': '0.234422%', 'stx': '0.217776%', 'swks': '0.217237%', 'hpe': '0.214042%',
                            'vrsn': '0.200256%', 'tdy': '0.190205%', 'ntap': '0.188758%', 'tyl': '0.186817%',
                            'flt': '0.184665%', 'enph': '0.183556%', 'ter': '0.179974%', 'akam': '0.178284%',
                            'trmb': '0.170798%', 'br': '0.166634%', 'mpwr': '0.166281%', 'nlok': '0.159129%',
                            'wdc': '0.156165%', 'payc': '0.152895%', 'qrvo': '0.136891%', 'ctxs': '0.122639%',
                            'sedg': '0.122325%', 'jkhy': '0.119720%', 'ffiv': '0.118357%', 'ptc': '0.117606%',
                            'jnpr': '0.109126%', 'cday': '0.101294%', 'dxc': '0.091008%', 'ipgp': '0.051372%'}
            self.ticker_string = ticker
            self.is_real_etf = True

        elif ticker == 'xlv' or ticker == 'rxl' or ticker == 'cure':  # Hardcoded more than top 25 XLV (Healthcare) holdings
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
            self.ticker_string = ticker
            self.is_real_etf = True

        elif ticker == 'vht':  # Hardcoded more than top 25 Vanguard VHT (Healthcare) holdings
            self.weights = {'unh': '7.46%', 'jnj': '7.10%', 'pfe': '5.22%', 'tmo': '4.14%', 'abt': '3.93%',
                            'abbv': '3.77%', 'lly': '3.54%', 'dhr': '3.33%', 'mrk': '3.06%', 'mdt': '2.19%',
                            'bmy': '2.18%', 'cvs': '2.15%', 'isrg': '2.02%', 'amgn': '2.01%', 'zts': '1.82%',
                            'antm': '1.78%', 'syk': '1.43%', 'mrna': '1.37%', 'gild': '1.36%', 'ew': '1.27%',
                            'ci': '1.23%', 'bdx': '1.14%', 'regn': '1.05%', 'hca': '1.04%', 'bsx': '0.95%',
                            'hum': '0.94%', 'vrtx': '0.90%', 'idxx': '0.88%', 'ilmn': '0.88%', 'iqv': '0.85%',
                            'dxcm': '0.82%', 'algn': '0.78%', 'a': '0.76%', 'cnc': '0.76%', 'bax': '0.68%',
                            'mtd': '0.62%', 'mck': '0.61%', 'rmd': '0.60%', 'biib': '0.56%', 'veev': '0.56%',
                            'wst': '0.55%', 'lh': '0.48%', 'cern': '0.43%', 'zbh': '0.42%', 'ste': '0.38%',
                            'hznp': '0.36%', 'wat': '0.36%', 'pki': '0.36%', 'avtr': '0.35%', 'ctlt': '0.34%',
                            'dgx': '0.33%', 'sgen': '0.33%', 'abc': '0.33%', 'coo': '0.33%', 'tech': '0.32%',
                            'alny': '0.32%', 'holx': '0.31%', 'crl': '0.30%', 'moh': '0.29%', 'podd': '0.29%',
                            'bio': '0.26%', 'vtrs': '0.26%', 'abmd': '0.26%', 'bmrn': '0.26%', 'tfx': '0.24%',
                            'masi': '0.24%', 'cah': '0.24%', 'rgen': '0.22%', 'incy': '0.22%', 'rprx': '0.21%',
                            'exas': '0.21%', 'tdoc': '0.21%', 'xray': '0.19%', 'elan': '0.19%', 'txg': '0.18%',
                            'hsic': '0.17%', 'synh': '0.17%', 'nvax': '0.16%', 'pen': '0.16%', 'uhs': '0.16%',
                            'uthr': '0.15%', 'tndm': '0.15%', 'brkr': '0.14%', 'gh': '0.14%', 'che': '0.13%',
                            'bhvn': '0.13%', 'nbix': '0.13%', 'ntra': '0.12%', 'omcl': '0.12%', 'ntla': '0.12%'}
            self.ticker_string = ticker
            self.is_real_etf = True

        elif ticker == 'xlf' or ticker == 'fas':  # Hardcoded more than top 25 XLF (Financials) holdings
            self.weights = {'jpm': '10.086%', 'bac': '7.675%', 'wfc': '5.049%', 'ms': '3.37%',
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
            self.ticker_string = ticker
            self.is_real_etf = True

        elif ticker == 'xlu' or ticker == 'utsl':  # Hardcoded more than top 25 XLU (Utilities) holdings
            self.weights = {'nee': '15.297%', 'duk': '8.344%', 'so': '7.551%', 'd': '6.751%', 'aep': '4.674%',
                            'sre': '4.502%', 'exc': '4.408%', 'xel': '3.85%', 'peg': '3.491%', 'ed': '3.166%',
                            'es': '3.115%', 'wec': '3.106%', 'awk': '2.942%', 'eix': '2.4%', 'dte': '2.393%',
                            'fe': '2.386%', 'aee': '2.333%', 'etr': '2.315%', 'ppl': '2.293%', 'cms': '1.927%',
                            'cnp': '1.821%', 'ceg': '1.799%', 'evrg': '1.553%', 'lnt': '1.542%', 'aes': '1.493%',
                            'ato': '1.455%', 'ni': '1.202%', 'nrg': '0.993%', 'pnw': '0.82%'}
            self.ticker_string = ticker
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

        elif ticker == 'soxx' or ticker == 'usd' or ticker == 'soxl':  # Hardcoded more than top 25 SOXX (Semiconductors) holdings
            self.weights = {'avgo': '9.33%', 'qcom': '8.82%', 'nvda': '6.52%', 'intc': '6.26%', 'amd': '4.84%',
                            'mu': '4.34%', 'mrvl': '4.29%', 'tsm': '4.28%', 'amat': '4.12%', 'klac': '4.07%',
                            'txn': '4.06%', 'adi': '4.0%', 'nxpi': '3.95%', 'xlnx': '3.95%', 'lrcx': '3.85%',
                            'mchp': '3.77%', 'asml': '3.42%', 'on': '2.23%', 'swks': '2.14%', 'ter': '1.7%',
                            'mpwr': '1.6%', 'entg': '1.59%', 'qrvo': '1.32%', 'stm': '1.24%', 'wolf': '0.97%',
                            'mksi': '0.77%', 'umc': '0.73%', 'lscc': '0.69%', 'oled': '0.57%', 'asx': '0.47%'}
            self.ticker_string = ticker
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

        elif ticker == 'vtwo':  # Vanguard Russell 2000
            self.weights = {'amc': '0.46%', 'syna': '0.37%', 'lscc': '0.34%', 'egp': '0.30%', 'bj': '0.30%',
                            'ttek': '0.30%', 'saia': '0.29%', 'ovv': '0.29%', 'thc': '0.28%', 'wsc': '0.28%',
                            'car': '0.28%', 'stag': '0.28%', 'slab': '0.27%', 'ntla': '0.27%', 'm': '0.27%',
                            'omcl': '0.26%', 'bhvn': '0.25%', 'crox': '0.25%', 'iivi': '0.24%', 'foxf': '0.24%',
                            'amba': '0.23%', 'pfgc': '0.23%', 'eme': '0.22%', 'chk': '0.22%', 'kbr': '0.22%',
                            'arwr': '0.22%', 'rpd': '0.22%', 'ffin': '0.22%', 'sgms': '0.21%', 'medp': '0.21%',
                            'trno': '0.21%', 'asgn': '0.21%', 'bpmc': '0.21%', 'gbci': '0.20%', 'txrh': '0.20%',
                            'iipr': '0.20%', 'novt': '0.20%', 'insp': '0.20%', 'expo': '0.20%', 'ssd': '0.20%',
                            'swav': '0.20%', 'gt': '0.19%', 'hele': '0.19%', 'wcc': '0.19%', 'gtls': '0.19%',
                            'amn': '0.19%', 'smtc': '0.19%', 'arna': '0.19%', 'roll': '0.19%', 'nsa': '0.18%',
                            'bl': '0.18%', 'powi': '0.18%', 'cade': '0.18%', 'ssb': '0.18%', 'wk': '0.18%',
                            'halo': '0.18%', 'ufpi': '0.18%', 'apps': '0.18%', 'vly': '0.18%', 'ccmp': '0.18%',
                            'bcpc': '0.18%', 'aqua': '0.18%', 'mxl': '0.18%', 'wts': '0.18%', 'asan': '0.17%',
                            'hli': '0.17%', 'vrns': '0.17%', 'apg': '0.17%', 'wing': '0.17%', 'spsc': '0.17%',
                            'atkr': '0.17%', '—': '0.17%', 'rog': '0.17%', 'cit': '0.17%', 'avnt': '0.17%',
                            'tenb': '0.17%', 'trup': '0.17%', 'vg': '0.16%', 'ar': '0.16%', 'rhp': '0.16%',
                            'esnt': '0.16%', 'onto': '0.16%', 'adc': '0.16%', 'mms': '0.16%', 'neog': '0.16%',
                            'irdm': '0.16%', 'sigi': '0.16%', 'mime': '0.16%', 'bxmt': '0.16%', 'jbt': '0.16%'}
            self.ticker_string = 'vtwo'
            self.is_real_etf = True

        elif ticker == 'xlc':  # XLC - SPY Communications sector
            self.weights = {'googl': '23.8290%', 'fb': '17.8399%', 't': '5.2009%', 'vz': '5.1836%', 'tmus': '5.0897%',
                            'atvi': '5.0472%', 'cmcsa': '4.9552%', 'chtr': '4.8334%', 'dis': '4.4452%',
                            'nflx': '3.2145%', 'ea': '3.1868%', 'mtch': '2.6019%', 'twtr': '2.2630%',
                            'viac': '1.6483%', 'ttwo': '1.5426%', 'omc': '1.3552%', 'ipg': '1.1813%',
                            'lyv': '1.1736%', 'foxa': '1.0754%', 'lumn': '0.9538%', 'nwsa': '0.7242%',
                            'disck': '0.7132%', 'dish': '0.6319%', 'fox': '0.4520%', 'disca': '0.4018%',
                            'nws': '0.2253%'}
            self.ticker_string = 'xlc'
            self.is_real_etf = True

        elif ticker == 'ihi':  # IHI - Medical Devices
            self.weights = {'tmo': '16.36%', 'abt': '16.02%', 'mdt': '9.71%', 'bdx': '5.36%', 'bsx': '4.94%',
                            'syk': '4.66%', 'ew': '4.56%', 'isrg': '4.1%', 'idxx': '3.54%', 'bax': '3.51%',
                            'dxcm': '3.29%', 'rmd': '2.79%', 'zbh': '1.88%', 'ste': '1.83%', 'wat': '1.61%',
                            'holx': '1.5%', 'podd': '1.35%', 'tfx': '1.19%', 'bio': '1.09%', 'abmd': '1.06%',
                            'masi': '0.91%', 'pen': '0.63%', 'tndm': '0.6%', 'brkr': '0.55%', 'nvst': '0.55%',
                            'nvcr': '0.52%', 'gmed': '0.43%', 'swav': '0.43%', 'iart': '0.38%', 'cnmd': '0.32%',
                            'livn': '0.32%', 'irtc': '0.3%', 'staa': '0.28%', 'atrc': '0.24%', 'itgr': '0.21%',
                            'gkos': '0.21%', 'nuva': '0.21%', 'nari': '0.19%', 'axnx': '0.19%', 'nvro': '0.18%',
                            'ocdx': '0.15%', 'cyrx': '0.14%', 'nstg': '0.13%', 'om': '0.12%',
                            'sens': '0.12%', 'hska': '0.12%', 'mlab': '0.11%', 'vrex': '0.08%', 'xent': '0.07%',
                            'lmat': '0.07%', 'ango': '0.06%', 'ntus': '0.06%', 'bfly': '0.06%', 'csii': '0.06%',
                            'aort': '0.06%', 'ingn': '0.05%', 'ofix': '0.05%', 'vray': '0.05%',
                            'srdx': '0.05%', 'sibn': '0.04%', 'tmdx': '0.03%', 'spne': '0.03%', 'vapo': '0.03%',
                            'axgn': '0.03%'}
            self.ticker_string = 'ihi'
            self.is_real_etf = True

        elif ticker == 'metv':  # Metaverse ETF
            self.weights = {'aapl': '4.35%', 'adbe': '1.14%', 'adsk': '3.81%', 'akam': '1.09%', 'amd': '2.92%',
                            'amzn': '4.13%', 'atvi': '0.79%', 'baba': '0.91%', 'bsy': '0.60%', 'coin': '1.24%',
                            'dis': '1.24%', 'ea': '1.97%', 'eqix': '0.47%', 'fb': '6.25%', 'fsly': '1.90%',
                            'googl': '1.93%', 'intc': '1.49%', 'llnw': '0.75%', 'lumn': '1.17%', 'msft': '7.18%',
                            'mttr': '0.70%', 'net': '0.84%', 'nke': '0.50%', 'nvda': '8.46%', 'pl': '0.40%',
                            'ptc': '0.69%', 'pypl': '0.11%', 'qcom': '3.89%', 'rblx': '5.47%', 'se': '3.21%',
                            'snap': '4.58%', 'sq': '0.10%', 'swks': '0.97%', 'tsm': '4.41%', 'ttwo': '2.66%',
                            'u': '5.05%'}
            self.ticker_string = 'metv'
            self.expense_ratio = '0.59%'
            self.is_real_etf = True

        elif ticker == 'vpn':  # VPN Expense Ratio
            self.weights = {'amt': '12.19%', 'cci': '12.02%', 'eqix': '11.71%', 'dlr': '8.67%',
                            'cone': '4.78%', 'sbac': '4.53%', 'gds': '4.35%', 'swch': '3.81%',
                            'unit': '3.28%',
                            'amd': '2.04%', 'nvda': '1.99%',
                            'mchp': '1.9%', 'intc': '1.87%', 'mu': '1.86%', 'vnet': '1.17%',
                            'radi': '1.14%', 'cyxt': '0.84%'}
            self.ticker_string = 'vpn'
            self.expense_ratio = '0.59%'
            self.is_real_etf = True

        elif ticker == 'lawp':  # My Leveraged All Weather Portfolio
            self.weights = {'tqqq': '45.00%', 'fngu': '2.00%', 'bulz': '2.00%', 'fngg': '2.00%', 'soxl': '2.00%',
                            'tecl': '2.00%', 'rom': '2.00%', 'upro': '2.00%', 'cure': '3.00%', 'fas': '1.00%',
                            'vpu': '1.00%', 'vig': '1.00%', 'xbi': '1.00%', 'ihi': '1.00%', 'coin': '1.00%',
                            'voog': '1.00%', 'vdc': '1.00%', 'vgt': '1.00%', 'vox': '1.00%', 'vht': '1.00%',
                            'schg': '1.00%',
                            'v': '1.00%', 'ma': '1.00%', 'amzn': '1.00%', 'googl': '1.00%',
                            'fb': '1.00%', 'msft': '1.00%', 'aapl': '1.00%', 'nflx': '1.00%',
                            'adbe': '1.00%', 'tsm': '1.00%', 'crm': '1.00%', 'amt': '1.00%',
                            'dlr': '1.00%', 'cci': '1.00%', 'sbac': '1.00%', 'eqix': '1.00%', 'tmf': '20.00%'}
            self.ticker_string = 'lawp'

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
        self.num_holdings = str(len(self.components))

        # Query Finviz metrics for real ETFs
        if self.is_real_etf:
            finviz_fundamentals = get_finviz_metrics(ticker, ['Company', 'Dividend %', 'Price', 'SMA20', 'SMA50', 'SMA200', '52W High', 'Perf Year', 'Volatility M'])

            if finviz_fundamentals is not None:
                self.name = finviz_fundamentals['Company']
                self.dividend_yield = finviz_fundamentals['Dividend %']
                self.price = finviz_fundamentals['Price']
                self.sma20 = finviz_fundamentals['SMA20']
                self.sma50 = finviz_fundamentals['SMA50']
                self.sma200 = finviz_fundamentals['SMA200']
                self.high_52W = finviz_fundamentals['52W High']
                self.perf_year = finviz_fundamentals['Perf Year']
                self.monthly_volatility = finviz_fundamentals['Volatility M']

        if self.leverage is None:
            try:
                if '3x' in self.name or '3X' in self.name or 'ProShares UltraPro' in self.name:
                    self.leverage = '3x'
                elif '2x' in self.name or '2X' in self.name or 'ProShares Ultra' in self.name:
                    self.leverage = '2x'
                else:
                    self.leverage = '1x'
            except Exception as e:
                pass

        # Try setting expense ratio
        if self.expense_ratio is None:
            try:
                url = 'https://www.marketwatch.com/investing/fund/%s?mod=mw_quote_tab' % self.ticker
                html_doc = requests.get(url).text
                self.expense_ratio = re.findall('(?<=<small class="label">Net Expense Ratio).*\n.*([0-9]{1}.[0-9]{2}%)(?=<\/span>)', html_doc)[0]
            except Exception as e:
                self.expense_ratio = None

        # Weighted Median EV/GP
        relative_EV_to_GPs = []
        for ticker in self.weights.keys():
            try:
                for i in range(int(to_number(self.weights[ticker]) * 1000)):
                    if self.components[ticker].ev_to_gp_ratio is not None:
                        relative_EV_to_GPs.append(self.components[ticker].ev_to_gp_ratio)
                    else:
                        relative_EV_to_GPs.append('1000000.00')
            except Exception as e:
                pass
        try:
            self.weighted_median_EV_to_GP = get_median_from_list(relative_EV_to_GPs)
            if self.weighted_median_EV_to_GP == '1000000.00':
                self.weighted_median_EV_to_GP = None
        except Exception as e:
            self.weighted_median_EV_to_GP = None

        # Weighted Median Adj. EV/EBIT
        relative_adj_EV_to_EBITs = []
        for ticker in self.weights.keys():
            try:
                for i in range(int(to_number(self.weights[ticker]) * 1000)):
                    if self.components[ticker].adj_ev_to_ebit_ratio is not None:
                        relative_adj_EV_to_EBITs.append(self.components[ticker].adj_ev_to_ebit_ratio)
                    else:
                        relative_adj_EV_to_EBITs.append('1000000.00')
            except Exception as e:
                pass
        try:
            self.weighted_median_adj_EV_to_EBIT = get_median_from_list(relative_adj_EV_to_EBITs)
            if self.weighted_median_adj_EV_to_EBIT == '1000000.00':
                self.weighted_median_adj_EV_to_EBIT = None
        except Exception as e:
            self.weighted_median_adj_EV_to_EBIT = None

        # Median Adj Rev Growth
        rev_growth = []
        for ticker in self.weights.keys():
            try:
                for i in range(int(to_number(self.weights[ticker]) * 1000)):
                    if self.components[ticker].adj_rev_growth_3y is not None:
                        rev_growth.append(self.components[ticker].adj_rev_growth_3y)
            except Exception as e:
                pass
        try:
            self.adj_rev_growth_3y = get_median_from_list(rev_growth)
        except Exception as e:
            self.adj_rev_growth_3y = None

        # Weighted Median "Median Revenue Growth 3Y"
        relative_med_rev_growth = []
        for ticker in self.weights.keys():
            try:
                for i in range(int(to_number(self.weights[ticker]) * 1000)):
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
                for i in range(int(to_number(self.weights[ticker]) * 1000)):
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
                for i in range(int(to_number(self.weights[ticker]) * 1000)):
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
                for i in range(int(to_number(self.weights[ticker]) * 1000)):
                    if self.components[ticker].ebit_margin is not None:
                        relative_med_ebit_margin.append(self.components[ticker].ebit_margin)
            except Exception as e:
                pass
        try:
            self.weighted_med_ebit_margin = get_median_from_list(relative_med_ebit_margin)
        except Exception as e:
            self.weighted_med_ebit_margin = None

        # Weighted Median Price to FVE
        price_to_FVEs = []
        for ticker in self.weights.keys():
            try:
                for i in range(int(to_number(self.weights[ticker]) * 1000)):
                    if self.components[ticker].price_to_FVE is not None:
                        price_to_FVEs.append(self.components[ticker].price_to_FVE)
            except Exception as e:
                pass
        try:
            self.price_to_FVE = get_median_from_list(price_to_FVEs)
        except Exception as e:
            self.price_to_FVE = None

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
            self.percent_at_high = None
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
            self.percent_at_low = None
        else:
            self.percent_at_low = to_percent_string(numer / denom)

        # Weighted % positive revenue growth
        numer = 0
        numer_high = 0
        denom = 0

        for ticker in self.weights.keys():
            try:
                if self.components[ticker].adj_rev_growth_3y is not None:
                    if to_number(self.components[ticker].adj_rev_growth_3y) > 0:  # Positive revenue growth
                        numer += to_number(self.weights[ticker])
                    if to_number(self.components[ticker].adj_rev_growth_3y) >= 0.07:  # Rev growth of at least 7%
                        numer_high += to_number(self.weights[ticker])
                    denom += to_number(self.weights[ticker])
            except Exception as e:
                pass
        if denom == 0:
            self.percent_positive_rev_growth = None
            self.percent_above_average_rev_growth = None
        else:
            self.percent_positive_rev_growth = to_percent_string(numer / denom)
            self.percent_above_average_rev_growth = to_percent_string(numer_high / denom)

        # Weighted % positive ebit margin
        numer = 0
        denom = 0

        for ticker in self.weights.keys():
            try:
                if self.components[ticker].ebit_margin is not None and to_number(self.components[ticker].ebit_margin) > 0:
                    numer += to_number(self.weights[ticker])
                denom += to_number(self.weights[ticker])
            except Exception as e:
                pass
        if denom == 0:
            self.percent_positive_ebit_margin = None
        else:
            self.percent_positive_ebit_margin = to_percent_string(numer / denom)

        try:
            self.percent_three_largest_holdings = to_percent_string(sum(sorted(to_number(x) for x in self.weights.values())[-3:]) / sum(to_number(x) for x in self.weights.values()))
        except Exception as e:
            self.percent_three_largest_holdings = None

        try:
            multiplier = int(self.leverage[0])
            self.leveraged_adj_rev_growth_3y = to_percent_string(multiplier * to_number(self.adj_rev_growth_3y))
        except Exception as e:
            self.leveraged_adj_rev_growth_3y = None

        # Generate "Martin" Score - my arbitrary scoring system for finding ETFs I like
        martin_score = 0

        # % stocks with positive rev growth
        try:
            if to_number(self.percent_positive_rev_growth) >= 0.90:
                martin_score += 1
        except Exception as e:
            pass

        # % stocks with positive rev growth
        try:
            if to_number(self.percent_positive_rev_growth) >= 0.95:
                martin_score += 1
        except Exception as e:
            pass

        # 80% of stocks have at least 7% rev growth
        try:
            if to_number(self.percent_above_average_rev_growth) >= 0.80:
                martin_score += 1
        except Exception as e:
            pass

        # Revenue growth > 8%
        try:
            if to_number(self.adj_rev_growth_3y) >= 0.08:
                martin_score += 1
        except Exception as e:
            pass

        # Revenue growth > 15%
        try:
            if to_number(self.adj_rev_growth_3y) >= 0.15:
                martin_score += 1
        except Exception as e:
            pass

        # Revenue growth > 25%
        try:
            if to_number(self.adj_rev_growth_3y) >= 0.25:
                martin_score += 1
        except Exception as e:
            pass

        # EV/GP
        try:
            if to_number(self.weighted_median_EV_to_GP) <= 15.0:
                martin_score += 1
        except Exception as e:
            pass

        # EV/EBIT
        try:
            if to_number(self.weighted_median_adj_EV_to_EBIT) <= 30.0:
                martin_score += 1
        except Exception as e:
            pass

        # % of stocks with positive EBIT margin
        try:
            if to_number(self.percent_positive_ebit_margin) >= 0.70:
                martin_score += 1
        except Exception as e:
            pass

        # % of stocks with positive EBIT margin
        try:
            if to_number(self.percent_positive_ebit_margin) >= 0.90:
                martin_score += 1
        except Exception as e:
            pass

        # Median EBIT margin over 20%
        try:
            if to_number(self.weighted_med_adj_ebit_margin) >= 0.20:
                martin_score += 1
        except Exception as e:
            pass

        # Median Gross margin over 50%
        try:
            if to_number(self.weighted_med_gross_margin) >= 0.50:
                martin_score += 1
        except Exception as e:
            pass

        # For 1x - +1 point for low expense ratio
        try:
            if to_number(self.expense_ratio) <= 0.0022:
                martin_score += 1
        except Exception as e:
            pass

        # For 2x -> +1 point for vol under 5%
        # For 3x -> +1 point for vol under 6%
        try:
            if self.leverage == '2x' and to_number(self.monthly_volatility) <= 0.05:
                martin_score += 1
            elif self.leverage == '3x' and to_number(self.monthly_volatility) <= 0.06:
                martin_score += 1
        except Exception as e:
            pass

        # Sum 3 largest holdings
        try:
            if to_number(self.percent_three_largest_holdings) < 0.25:
                martin_score += 1
        except Exception as e:
            pass

        self.martin_score = str(martin_score)
        if self.num_holdings == '0':
            self.martin_score = None

    def fill_holdings_from_marketwatch(self, ticker):
        url = 'https://www.marketwatch.com/investing/fund/%s/holdings' % ticker
        html_doc = requests.get(url).text
        ticker_results = re.findall('(?<=<td class="table__cell u-semi">)([A-Z]+)(?=<\/td>)', html_doc)
        weightings_results = re.findall('(?<=<td class="table__cell">)([0-9]{1,3}.[0-9]{2}%)(?=<\/td>)', html_doc)
        self.weights = {ticker_results[i]: weightings_results[i] for i in range(len(ticker_results))}
        return

    # Takes space delimited list of tickers and set equal-weight holdings
    def set_components(self):
        with open('cache.txt', 'w+') as f:
            cache = dict(f.read())

        for ticker in self.weights.keys():
            try:  # Try to make the ticker a stock. If it is likely not a stock, it is probably an ETF.
                if 'USD' in ticker and ticker != 'USD':
                    self.components[ticker] = Crypto(ticker)
                else:
                    try:
                        self.components[ticker] = Stock(ticker)
                        if self.components[ticker].type == 'ETF':
                            self.components[ticker] = ETF(ticker)
                    except Exception as e:
                        # Some new ETFs not in Finviz can fall here
                        self.components[ticker] = ETF(ticker)
            except Exception as e:
                pass

    # For each stock in an ETF, displays data selected in columns
    def display_metrics(self, columns, only_nums=False, print_header=True, extra_header=False, include_overall=False):
        header = ''
        for metric_title in columns:
            header += metric_title + '\t'
        if extra_header:
            header += '=IF(C1="Stock", E1, IFERROR(0/0))\t=IF(C1="ETF", E1, IFERROR(0/0))\t=IF(C1="Stock", F1, IFERROR(0/0))\t=IF(C1="ETF", F1, IFERROR(0/0))\t'
        if print_header:
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
                        if metric_title == 'Num Holdings':
                            line += component.num_holdings + '\t'
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

                        if metric_title == 'Adj Rev Growth 3Y':
                            line += component.adj_rev_growth_3y + '\t'
                        if metric_title == 'Leveraged Rev Growth 3Y':
                            line += component.leveraged_adj_rev_growth_3y + '\t'

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
                        if metric_title == 'Volatility':
                            line += component.monthly_volatility + '\t'

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
                        if metric_title == '% Pos Rev Growth':
                            line += component.percent_positive_rev_growth + '\t'
                        if metric_title == '% >7% Rev Growth':
                            line += component.percent_above_average_rev_growth + '\t'
                        if metric_title == '% Pos EBIT Margin':
                            line += component.percent_positive_ebit_margin + '\t'

                        if metric_title == 'Leverage':
                            line += component.leverage + '\t'
                        if metric_title == 'Expense Ratio':
                            line += component.expense_ratio + '\t'
                        if metric_title == 'Martin Score':
                            line += component.martin_score + '\t'

                        if metric_title == 'Price to FVE':
                            line += component.price_to_FVE + '\t'
                        if metric_title == 'Morningstar FVE':
                            line += component.morningstar_FVE + '\t'

                    except Exception as e:
                        line += '' + '\t'

                if only_nums:
                    line = ''.join(x for i, x in enumerate(line) if i-1 < 0 or x not in 'BMK' or line[i-1] not in '1234567890')
                print(line)

            except Exception as e:
                pass

    def display_summary(self):
        print(self.ticker, '-', self.name)
        print('Leverage:', self.leverage)
        print('Expense Ratio:', self.expense_ratio)
        print('Num Holdings Analyzed:', self.num_holdings)
        print('Growth')
        print('\tMedian Rev Growth:', self.adj_rev_growth_3y)
        print('\t% of holdings with positive revenue growth:', self.percent_positive_rev_growth)
        print('\t% of holdings with revenue growth above 7.00%:', self.percent_above_average_rev_growth)
        print('Valuation')
        print('\tMedian Gross Margin:', self.weighted_med_gross_margin)
        print('\tMedian Operating (EBIT) Margin:', self.weighted_med_adj_ebit_margin)
        print('\tMedian EV/GP:', self.weighted_median_EV_to_GP)
        print('\tMedian EV/EBIT:', self.weighted_median_adj_EV_to_EBIT)
        print('\tCurrent drawdown from the 52W High:', self.high_52W)
        print('Health')
        print('\t% of holdings with positive EBIT margin:', self.percent_positive_ebit_margin)
        print('\t% of holdings at 52W High (within 5%):', self.percent_at_high)
        print('\t% of holdings at 52W Low (within 5%):', self.percent_at_low)
        print('\t% of ETF covered by 3 largest holdings:', self.percent_three_largest_holdings)
        print('\nOverall "Martin" Score (out of 14):', self.martin_score)
