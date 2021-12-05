from finvizfinancefulfillment import *


class Ticker:

    def __init__(self, name):
        self.name = name

        fundamentals = get_finviz_metrics(name, ['Sales', 'Sales Q/Q'])

        self.revenue = fundamentals['Sales']
        self.revenue_growth = fundamentals['Sales Q/Q']
