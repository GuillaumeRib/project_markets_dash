# US Markets Dashboard

Interactive multi-page dashboard for analysing US equity and rates markets, built
with Plotly Dash. Featured in Plotly's selection of top finance applications.

**Live app:** https://markets-dash.onrender.com/

## What it does

- **S&P 500 performance** — analysis by sector and sub-industry, using
  constituent-level daily prices and IVV ETF weights
- **US Treasury yield curve** — from 3-month to 30-year maturities
- **PCA & clustering** — unsupervised analysis of S&P 500 constituents based on
  daily total returns over a rolling 2-year window: principal component analysis
  followed by K-Means clustering, grouping stocks by co-movement rather than by
  GICS sector
- Interactive Plotly charts across multiple pages

The PCA and clustering work started as a standalone project
([project_equity_clustering](https://github.com/GuillaumeRib/project_equity_clustering))
and was later integrated as a page of this app.

## Data sources

| Source | Data |
|---|---|
| FRED (pandas-datareader) | Monthly US Treasury yields, 3M to 30Y |
| yfinance | Daily prices for S&P 500 constituents |
| Wikipedia (scraping) | S&P 500 tickers, sectors, sub-industries |
| IVV ETF | Index constituent weights |

## Stack

Python · pandas · scikit-learn · Plotly · Dash · pandas-datareader · yfinance · BeautifulSoup
Deployed on Render.

