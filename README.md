# financial-metric-scraper
Web scraper for collecting financial data from various online sources. Acts as a data fulfillment orchestrator for building financial models.

Goals
* Able to provide weighted ETF metrics based on the underlying holdings. For example, a weighted Sales Q/Q growth would take the weighted arithmetic mean of the individual holdings of an ETF. 

scraper.py would collect the necessary data online (weighted holdings of the ETF, Sales Q/Q data of the individual stocks)
metrics.py provides an interface over the data scraping and aggregation layer. metrics.py contains a collection of callable functions for returning basic financial metrics (Price, Sales, Earnings, etc.) as well as derived financial metrics (P/E, P/S, etc.)
