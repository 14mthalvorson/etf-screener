# A financial screener for public stocks and ETFs

This project was designed for my personal use to aggregate financial data from a collection of sources, calculate some new metrics, and output the data in a convenient format for using in Excel or Google Sheets. After manually collecting this data many times, I wanted to automate all of these processes to save time, improve accuracy, and provide a platform for further building off of.

## Current Data Sources
- Yahoo finance (from the yfinance Python library)
- Finviz finance (from the finviz Python library)
- Macrotrends (scraped from the website using requests library)
- Marketwatch (scraped from the website using requests library)

## Current Capabilities
#### Pulls financial metrics for individual stocks from different sources
- Examples from [Finviz](https://finviz.com/quote.ashx?t=AAPL): Market Cap, Revenue, P/E, P/S, Gross/Operating/Net Margins, Drawdown from 52W High, Stock Performance Data
- Examples from [Macrotrends](https://www.macrotrends.net/stocks/charts/GOOGL/alphabet/revenue): Quarterly Revenue, EBITDA (and EBITDA Margin), Cash/Debt, historical P/S, PE Ratio
#### Pulls ETF holdings data from [Marketwatch](https://www.marketwatch.com/investing/fund/qqq/holdings)
#### Calculates aggregate ETF metrics based on the financial metrics of the underlying holdings
- Example: Calculate "Weighted 3Y Revenue Growth" for QQQ, SPY, or VIG
#### Calculates new financial metrics (not found in any of the data sources)
Example: Calculate the "Median 3Y Quarterly Revenue Growth" and the "Enterprise Value to EBIT ratio" for the holdings of QQQ
1. Look up QQQ holdings in Marketwatch (top 25)
2. For each of these stocks, pull the last 3 years of quarterly revenue growth rates from Macrotrends. Calculate the medians.
3. Pull the market caps from finviz. Pull the cash, debt, revenue, and operating (EBIT) margin from Macrotrends. Calculate the individual EVs, then EV/EBIT ratios.
4. Using the Median 3Y Quarterly Revenue Growth" and "Enterprise Value to EBIT ratio" for each of the individual holdings, calculating the weighted metric for the overall ETF.
#### Outputs results in an Excel-friendly tab-delimited format
- Can just simply copy/paste the data into Excel or Google Sheets to graph the results. In the long-run, I can automate this too if I wanted but the time savings here isn't worth automation yet...

## Future Goals
- Improve data sources for international stocks
- Add conditional statements for filtering lists of stocks (e.g. show revenue growth for QQQ holdings where Operating Margin > 10%)
- Review and add more error handling


