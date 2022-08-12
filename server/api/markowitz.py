import datetime

from flask import jsonify
from flask_apispec import MethodResource, marshal_with, use_kwargs
from flask_restful import Resource
from server.api.myResponses import InputSchema
from server.dto.responseApi import ResponseApi
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_datareader import data as web
from functools import reduce
from tabulate import tabulate
from matplotlib.ticker import FormatStrFormatter


class Markowitz(MethodResource, Resource):
    def importing(self):
        # 1 - Define `tickers` & `company names` for every instrument
        stocks = {'AAPL': 'Apple', 'MSFT': 'Microsoft', 'AMZN': 'Amazon', 'GOOG': 'Google', 'FB': 'Facebook',
                  'NFLX': 'Netflix', 'NVDA': 'NVIDIA'}
        bonds = {'HCA': 'HCA', 'VRTX': 'VRTX'}
        commodities = {'BTC-USD': 'Bitcoin', 'PA=F': 'Palladium'}
        instruments = {**stocks, **bonds, **commodities}
        tickers = list(instruments.keys())
        instruments_data = {}
        N = len(tickers)

        # 2 - We will look at stock prices over the past years, starting at January 1, 2015
        #                               01-01-2015 - 16-04-2020
        start = datetime.datetime(2015, 1, 1)
        end = datetime.datetime(2020, 4, 16)

        # 3 - Let's get instruments data based on the tickers.
        # First argument is the series we want, second is the source ("yahoo" for Yahoo! Finance), third is the start date, fourth is the end date
        for ticker, instrument in instruments.items():
            print("Loading data series for instrument {} with ticker = {}".format(instruments[ticker], ticker))
            instruments_data[ticker] = web.DataReader(ticker, data_source='yahoo', start=start, end=end)
        ## 2.3.1 - keep only `adjusted close` prices
        for ticker, instrument in instruments.items():
            instruments_data[ticker] = instruments_data[ticker]["Adj Close"]
            ## 2.3.2 - Drop duplicates for palladium data from Yahoo Source
        instruments_data['PA=F'] = instruments_data['PA=F'].drop_duplicates()

        tr_days = [len(instr) for _, instr in instruments_data.items()]
        tr_days = pd.DataFrame(tr_days, index=tickers, columns=["Trading Days"])

        tr_days_stocks_bonds = instruments_data['AAPL'].groupby([instruments_data['AAPL'].index.year]).agg('count')
        tr_days_bitcoin = instruments_data['BTC-USD'].groupby([instruments_data['BTC-USD'].index.year]).agg('count')
        tr_days_palladium = instruments_data['PA=F'].groupby([instruments_data['PA=F'].index.year]).agg('count')

        tr_days_per_year = pd.DataFrame([tr_days_stocks_bonds, tr_days_bitcoin, tr_days_palladium],
                                        index=["Stocks & Bonds", "Bitcoin", "Palladium"])

        ## 2.4 - Merging Dataframes
        '''
            instruments_data = {'AAPL' : dataframe (1331 x 1),..., 'BTC-USD' : dataframe (1934 x 1), 'PA=F' : dataframe (1336 x 1)}
            [*] So list(instruments_data.values()) : we only keep the dataframes in a list
            [*] data_df = pd.concat(data, axis = 1).dropna() DID not wor because of different `commodities` sizes
    
        '''
        data = list(instruments_data.values())
        data_df = reduce(lambda x, y: pd.merge(x, y, left_index=True, right_index=True, how='outer'), data).dropna()
        data_df.columns = tickers





    @marshal_with(InputSchema)  # marshalling with marshmallow library
    @use_kwargs(InputSchema, location=('query'))
    def get(self, amountToInvest, riskScore):
        volatilityPercentage = 40
        self.get_optimal_portfolio()
        stokes = [{'BTC': 10000}, {'ETH': 10000}, {'XRP': 10000}, {'LTC': 10000}, {'BCH': 10000}, {'EOS': 10000}]
        response = ResponseApi("GiniWithML", volatilityPercentage, stokes, amountToInvest, datetime.datetime.now())
        return jsonify(response.__str__())
        # return jsonify()
