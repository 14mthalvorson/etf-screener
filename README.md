# A financial screener for public stocks and ETFs

The main goal of this screener is to calculate weighted financial metrics for ETFs, similar to metrics you can easily find for stocks. These metrics are mainly around the growth rate, valuation, and general health of an ETF. The process of calculating these metrics includes scraping the weighted holdings (stocks) composing an ETF, pulling the financial data of these underlying holdings, running data validation checks, and performing the weighted metric calculations. The output is usually in a tab-separated format for an easy copy/paste into Excel or Google Sheets. This process originally started off with me manually doing a lot of this work and I figured I could automate much of this process to save time, improve accuracy, and provide a programmatic platform for further building off of. Additionally, the (primarily) ETF screener can also be used to screen stocks, for which there are many additional metrics not available for ETFs. This project was designed for my personal use (but feel free to use as well if useful!) and is not intended for use in any production systems.

[Financial Metrics Available and Data Sources](https://docs.google.com/spreadsheets/d/1DgvwIgLPSnxBZZrfBXDTJCxMmPCuiBNBMZJBUxu6hFE/edit?usp=sharing)

## Examples of Capabilities

### Example 1: Generate a summary for an ETF.

Input:
```
etf = ETF('qld')  # (2x QQQ)
etf.display_summary()
```

Output:
```
qld - ProShares Ultra QQQ
Leverage: 2x
Expense Ratio: 0.95%
Num Holdings Analyzed: 100
Growth
	Median Rev Growth: 14.18%
	% of holdings with positive revenue growth: 97.90%
	% of holdings with revenue growth above 7.00%: 83.62%
Valuation
	Median Gross Margin: 56.51%
	Median Operating (EBIT) Margin: 29.78%
	Median EV/GP: 13.06
	Median EV/EBIT: 25.42
	Current drawdown from the 52W High: -24.76%
Health
	% of holdings with positive EBIT margin: 96.11%
	% of holdings at 52W High (within 5%): 5.18%
	% of holdings at 52W Low (within 5%): 4.35%
	% of ETF covered by 3 largest holdings: 30.83%

Overall "Martin" Score (out of 14): 10
```

### Example 2: Find the weighted median financial metrics for QQQ.

Rather than just relying on the metrics in the health summary, you can also select your own metrics to output.

Input:
```
etf = ETF('qqq')
columns = ['Ticker', 'Name', 'Type', 'Median Rev Growth 3Y', 'EV/GP', 'Adj EV/EBIT', 'Gross Margin', 'Adj EBIT Margin', '52W High', 'Weight']
etf.display_metrics(columns, include_overall=True)
```
The first line is a header. The second line has the aggregate metrics generated for the ETF specified. The following lines are the top holdings, with all the requested metrics listed. As noted above, the output is tab-separated format (which doesn't output as clearly here but it works very well in a spreadsheet). 

Output:
```
Ticker	Name	Type	Median Rev Growth 3Y	EV/GP	Adj EV/EBIT	Gross Margin	Adj EBIT Margin	52W High	Weight	
qqq	Invesco QQQ Trust	ETF	13.99%	15.52	24.92	56.50%	30.30%	-11.17%		
aapl	Apple Inc.	Stock	8.91%	17.76	24.92	41.80%	29.78%	-4.46%	11.69%	
adbe	Adobe Inc.	Stock	22.02%	17.07	41.00	88.20%	36.76%	-23.62%	1.8%	
adi	Analog Devices, Inc.	Stock	-1.62%	19.53	38.22	61.80%	31.61%	-14.58%	0.64%	
adp	Automatic Data Processing, Inc.	Stock	5.62%	13.05	24.58	42.50%	22.52%	-17.19%	0.63%	
amat	Applied Materials, Inc.	Stock	23.39%	11.06	17.51	47.30%	29.87%	-17.29%	0.95%	
amd	Advanced Micro Devices, Inc.	Stock	49.89%	18.83	43.49	46.80%	20.27%	-30.53%	1.16%	
amgn	Amgen Inc.	Stock	5.16%	7.49	13.06	75.40%	43.22%	-12.97%	0.96%	
amzn	Amazon.com, Inc.	Stock	26.39%	7.63	47.15	41.30%	6.68%	-20.72%	6.78%	
atvi	Activision Blizzard, Inc.	Stock	16.65%	8.41	17.43	72.60%	35.05%	-24.41%	0.46%	
avgo	Broadcom Inc.	Stock	10.03%	15.52	30.69	61.40%	31.03%	-13.56%	1.82%	
bkng	Booking Holdings Inc.	Stock	3.94%		28.67		36.77%	-8.60%	0.74%	
chtr	Charter Communications, Inc.	Stock	5.15%	8.14	18.54	44.70%	19.63%	-28.13%	0.79%	
cmcsa	Comcast Corporation	Stock	17.85%	3.98	13.26	67.00%	20.11%	-19.11%	1.53%	
cost	Costco Wholesale Corporation	Stock	12.39%	8.18	30.51	12.80%	3.43%	-11.61%	1.67%	
csco	Cisco Systems, Inc.	Stock	3.97%	6.69	15.32	63.70%	27.81%	-13.40%	1.78%	
csx	CSX Corporation	Stock	-1.47%	9.28	15.38	75.70%	45.66%	-9.97%	0.57%	
exc	Exelon Corporation	Stock	-2.23%	4.33	19.41	58.10%	12.98%	-0.11%	0.42%	
fb	Meta Platforms, Inc.	Stock	28.59%	8.80	15.95	80.90%	44.62%	-18.49%	4.78%	
fisv	Fiserv, Inc.	Stock	16.91%	10.78	18.14	50.70%	30.10%	-16.99%	0.52%	
gild	Gilead Sciences, Inc.	Stock	5.06%	4.73	8.99	80.50%	42.31%	-7.34%	0.65%	
googl	Alphabet Inc.	Stock	20.03%	11.92	22.22	56.50%	30.30%	-10.38%	7.19%	
hon	Honeywell International Inc.	Stock	-6.28%	12.69	21.59	32.30%	19.01%	-13.67%	0.96%	
intc	Intel Corporation	Stock	0.14%	4.59	7.72	55.40%	32.91%	-28.72%	1.39%	
intu	Intuit Inc.	Stock	14.67%	17.81	48.19	82.10%	30.30%	-22.55%	1.21%	
isrg	Intuitive Surgical, Inc.	Stock	17.45%	23.75	50.57	69.30%	32.56%	-23.13%	0.73%	
kdp	Keurig Dr Pepper Inc.	Stock	7.62%	9.33	22.67	56.40%	23.20%	-3.56%	0.40%	
klac	KLA Corporation	Stock	26.69%	11.69	18.45	61.80%	39.20%	-14.84%	0.42%	
lrcx	Lam Research Corporation	Stock	18.25%	11.34	16.89	46.20%	31.06%	-19.39%	0.59%	
mdlz	Mondelez International, Inc.	Stock	2.58%	9.70	23.45	39.20%	16.21%	-3.51%	0.69%	
meli	MercadoLibre, Inc.	Stock	66.40%	20.30	137.38	42.10%	6.26%	-43.59%	0.40%	
mrna	Moderna, Inc.	Stock		5.44	7.27	85.90%	64.33%	-65.96%	0.48%	
mrvl	Marvell Technology, Inc.	Stock	9.92%	32.88	81.08	45.90%	18.56%	-23.92%	0.41%	
msft	Microsoft Corporation	Stock	13.99%	17.19	28.07	68.80%	42.14%	-11.06%	10.13%	
mu	Micron Technology, Inc.	Stock	13.58%	7.23	6.40	41.50%	46.84%	-16.43%	0.66%	
nflx	Netflix, Inc.	Stock	24.88%	15.99	29.23	41.60%	22.76%	-39.07%	1.78%	
nvda	NVIDIA Corporation	Stock	49.90%	37.09	67.57	64.40%	35.34%	-29.33%	4.15%	
pep	PepsiCo, Inc.	Stock	5.72%	6.42	21.82	53.90%	15.87%	-2.10%	1.6%	
pypl	PayPal Holdings, Inc.	Stock	18.57%	16.18	44.91	47.80%	17.23%	-44.56%	1.47%	
qcom	QUALCOMM Incorporated	Stock	11.88%	9.97	17.59	57.50%	32.59%	-9.21%	1.36%	
regn	Regeneron Pharmaceuticals, Inc.	Stock	31.54%	5.11	8.03	86.60%	55.18%	-11.36%	0.49%	
sbux	Starbucks Corporation	Stock	7.03%	14.30	24.66	28.90%	16.76%	-22.17%	0.91%	
tmus	T-Mobile US, Inc.	Stock	6.38%	4.42	19.57	56.90%	12.85%	-27.98%	0.96%	
tsla	Tesla, Inc.	Stock	45.50%	68.36	180.79	25.30%	9.57%	-24.67%	4.26%	
txn	Texas Instruments Incorporated	Stock	-0.88%	13.00	18.67	67.50%	47.02%	-11.26%	1.16%	
vrtx	Vertex Pharmaceuticals Incorporated	Stock	33.44%	7.73	14.45	88.10%	47.15%	-0.10%	0.46%
```

### Example 3: You can compare multiple stocks and multiple ETFs at the same time.

Input:
```
etf = ETF('spy qqq vig aapl msft googl amzn fb')
columns = ['Ticker', 'Name', 'Type', 'Median Rev Growth 3Y', 'EV/GP', 'Adj EV/EBIT', 'Gross Margin', 'Adj EBIT Margin', '52W High']
etf.display_metrics(columns)
```

Output:
```
Ticker	Name	Type	Median Rev Growth 3Y	EV/GP	Adj EV/EBIT	Gross Margin	Adj EBIT Margin	52W High	Weight			
aapl	Apple Inc.	Stock	8.91%	17.76	24.92	41.80%	29.78%	-4.46%	
amzn	Amazon.com, Inc.	Stock	26.39%	7.63	47.15	41.30%	6.68%	-20.72%	
fb	Meta Platforms, Inc.	Stock	28.59%	8.80	15.95	80.90%	44.62%	-18.49%	
googl	Alphabet Inc.	Stock	20.03%	11.92	22.22	56.50%	30.30%	-10.38%	
msft	Microsoft Corporation	Stock	13.99%	17.19	28.07	68.80%	42.14%	-11.06%	
qqq	Invesco QQQ Trust	ETF	13.99%	15.52	24.92	56.50%	30.30%	-11.17%
spy	SPDR S&P 500 ETF Trust	ETF	13.99%	17.19	24.92	56.50%	29.78%	-6.26%	
vig	Vanguard Dividend Appreciation Index Fund ETF Shares	ETF	7.07%	10.14	21.59	57.00%	23.58%	-5.92%		
```

The sources for the financial data are listed in the spreadsheet linked at the top of the README. For the ETFs, the holdings are pulled from Marketwatch. Marketwatch only lists the top 25 holdings so that what most of the ETFs will use to analyze. I've hardcoded a few (QQQ, SPY, MOAT) beyond the top 25 that I use more frequently. This also helps during the times that Marketwatch is sometimes not available. I use a couple functions (clean tickers) in the utilities file to do this. Overall, it doesn't make much of a difference thankfully when calculating the weighted medians.

## "Martin" Scoring System

I just named it Martin so it's obvious this isn't some official scoring system but just something I made up. The scoring system is a simple sum, 1 point for each of the following:
- 90%+ stocks with positive revenue growth
- 95%+ stocks with positive revenue growth
- 80%+ stocks with 7%+ revenue growth
- 8%+ median revenue growth
- 15%+ median revenue growth
- 25%+ median revenue growth
- Median EV/GP lower than 15.0
- Median EV/EBIT lower than 30.0
- 70%+ stocks with positive EBIT margin
- 90%+ stocks with positive EBIT margin
- Median EBIT margin at least 20%
- Median gross margin at least 50%
- Expense Ratio is under 0.22%
- 3 Largest holdings make up less than 40% of the ETF


## Current Data Sources
[Data Sources](https://docs.google.com/spreadsheets/d/1DgvwIgLPSnxBZZrfBXDTJCxMmPCuiBNBMZJBUxu6hFE/edit?usp=sharing)
- Macrotrends (scraped from the website using requests library)
- Marketwatch (scraped from the website using requests library)
- Yahoo finance (from the Yahoo Finance and yfinance Python libraries)
- Finviz finance (from the finviz Python library)

## Required Libraries to Pip Install
- requests
- yfinance
- yahoofinance
- finvizfinance

## Assumptions
- I don't do automatic checks on the accuracy of data. Most of the numbers are pulled from Macrotrends and Finviz. The only discrepancies I notice are usually small differences in gross/operating/net margins. In the screener, I usually just average the two sources if they are both available. Maybe in the future I'll source and pull data directly from the SEC quarterly reports.

## Future Goals
- Add sourcing for expense ratios/fees
- Improve data sources for international stocks
- Add conditional statements for filtering lists of stocks (e.g. show revenue growth for QQQ holdings where Operating Margin > 10%)
- Review and add more error handling
- Adding some crypto metrics. Obvi crypto won't have the fundamentals stocks have but I could pull price data. Need to figure out the best API for this or the best place to scrape the data from.


