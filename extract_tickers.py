def generate_tickers(index = 'dowjones'):
    import requests                             #for making http requests to target server
    from bs4 import BeautifulSoup as bs         #for parsing http response 
    
    
    url = f"https://www.slickcharts.com/{index}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36", 
        "Accept-Language": "en-US,en;q=0.9"
            }
    
    page = requests.get(url, headers=headers)

    soup = bs(page.content, 'html.parser')

    table = soup.find('table', class_='table')

    ticker_rows = table.find_all('a')

    tickers = list(set([row.get('href').split('/')[-1] for row in ticker_rows]))
    
    return index, tickers


def get_stock_prices(index, ticker_list):
    
    import yfinance as yf                       #for pulling financial information - income statement

    data_parsed = {}
    for ticker in ticker_list:
        try:
            yf_ticker = yf.Tickers(ticker)
            data = yf_ticker.history(period="1d", group_by= 'tickers')
            data = data.reset_index()
            data_dict = data.to_dict(orient='records')
            data_parsed[ticker] = {
                'Date' : data_dict[0][('Date', '')].strftime('%Y-%m-%d'),
                'Ticker' : ticker,
                'Stock Index': index.upper(),
                'Open' : round(data_dict[0][(ticker, 'Open')], 5),
                'High' : round(data_dict[0][(ticker, 'High')], 5),
                'Low' : round(data_dict[0][(ticker, 'Open')], 5),
                'Close' : round(data_dict[0][(ticker, 'Open')], 5),
                'Volume' : data_dict[0][(ticker, 'Volume')],
                'Dividends' : data_dict[0][(ticker, 'Dividends')],
                'Stock Splits' : data_dict[0][(ticker, 'Stock Splits')]        
            }
        except Exception as e:
            print(e)
    return data_parsed
