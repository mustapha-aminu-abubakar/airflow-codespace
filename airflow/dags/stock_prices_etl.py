from airflow.models.dag import DAG
from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import yfinance as yf                       #for pulling financial information - income statement
from bs4 import BeautifulSoup as bs         #for parsing http response 
import requests                             #for making http requests to target server
import csv
import os

default_args = {
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

@dag(
    dag_id = 'stock_prices_etl',
    default_args=default_args,
    schedule= '0 0 * * Mon-Fri',
    start_date=datetime(2024, 11, 26),
)
def stock_prices_etl():
    
    @task(multiple_outputs=True)
    def generate_tickers(index = 'dowjones'):        
        
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
        
        return {'index': index, 'tickers': tickers}


    @task
    def get_stock_prices(index, ticker_list):
    
        index_list = {'sp500': 'SP500', 'nasdaq100': 'NDX100', 'dowjones': 'DJI30'}
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
                    'Stock Index': index_list[index],
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
    
    @task
    def load_data(data):
        csv_file = 'stock_prices'
        headers = [
            'Date',
            'Ticker',
            'Stock Index',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Dividends',
            'Stock Splits'            
        ]
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            writer.writerows(data.values())  # Appends multiple rows

    
    #dependencies
    sp500_tickers = generate_tickers('sp500')
    ndx100_tickers = generate_tickers('nasdaq100')    
    dji30_tickers = generate_tickers('dowjones')
    
    sp500_prices = get_stock_prices(*sp500_tickers.values())
    ndx100_prices = get_stock_prices(*ndx100_tickers.values())
    dji30_prices = get_stock_prices(*dji30_tickers.values())
    
    
    sp500_tickers >> sp500_prices
    ndx100_tickers >> ndx100_prices
    dji30_tickers >> dji30_prices
    
    [sp500_prices, ndx100_prices, dji30_prices] >> load_data()
   
    
stock_prices_etl = stock_prices_etl()
    
    
