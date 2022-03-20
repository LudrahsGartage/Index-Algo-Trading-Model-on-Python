# SP 500 Equal Weight Index Fund
# This script will accept a portfolio value and tell you how many shares of each snp constituent you must purchase to
# get an equal weight version of the index fund
# this script uses randomly generated data to avoid api costs, and creats an Excel file

import pandas as pd
import requests
import math

stocks = pd.read_csv('sp_500_stocks.csv')

IEX_CLOUD_API_TOKEN = 'Tpk_059b97af715d417d9f49f50b51b1c448'  # if using with actual data, keep stored in secrets.py

symbol = 'AAPL'
api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'

my_columns = ['Ticker', 'Price', 'Market Capitalization', 'Number Of Shares to Buy']


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

final_dataframe = pd.DataFrame(columns=my_columns)

for symbol_string in symbol_strings:
    #     print(symbol_strings)
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(
            pd.Series([symbol,
                       data[symbol]['quote']['latestPrice'],
                       data[symbol]['quote']['marketCap'],
                       'N/A'],
                      index=my_columns),
            ignore_index=True)

portfloio_size = input('enter the value of your portfolio')

try:
    val = float(portfloio_size)
    print(val)
except ValueError:
    print('please enter a number only')
    portfloio_size = input('enter the value of your portfolio')
    val = float(portfloio_size)
position_size = val/len(final_dataframe.index)
for i in range(0, len(final_dataframe.index)):
    final_dataframe.loc[i, 'Number Of Shares to Buy'] = math.floor(position_size/final_dataframe['Price'][i])

final_dataframe.to_csv('Recommended Trades.csv')
