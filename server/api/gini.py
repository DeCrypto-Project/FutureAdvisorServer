import datetime

from flask import request, jsonify
from flask_apispec import MethodResource, marshal_with, use_kwargs
from flask_restful import Resource, fields, reqparse

from server.api.myResponses import InputSchemaTwitter, InputSchema
import matplotlib.pyplot as plt

from server.dto.responseApi import ResponseApi

plt.switch_backend('Agg')
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np
from pandas_datareader import data as pdr


class Gini(MethodResource, Resource):

    def gini(self, volatile):
        # Select stocks, start year and end year, stock number has no known limit
        selected = ["SPY", "IEI", "LQD", "QQQ"]
        start_year = '2019-09-30'
        end_year = '2022-07-12'
        Num_porSimulation = 100
        V = volatile

        # Building the dataframe
        yf.pdr_override()
        frame = {}
        for stock in selected:
            data_var = pdr.get_data_yahoo(stock, start_year, end_year)['Adj Close']
            data_var.to_frame()
            frame.update({stock: data_var})

        import pandas as pd
        # Mathematical calculations, creation of 5000 portfolios,
        table = pd.DataFrame(frame)
        # pd.DataFrame(frame).to_csv('Out.csv')
        returns_daily = table.pct_change()
        port_profolio_annual = []
        port_gini_annual = []
        sharpe_ratio = []
        stock_weights = []

        # set the number of combinations for imaginary portfolios
        num_assets = len(selected)
        num_portfolios = Num_porSimulation

        # set random seed for reproduction's sake
        np.random.seed(101)

        # Mathematical calculations, creation of 5000 portfolios,
        table = pd.DataFrame(frame)
        # pd.DataFrame(frame).to_csv('Out.csv')
        returns_daily = table.pct_change()
        for stock in returns_daily.keys():
            table[stock + '_change'] = returns_daily[stock]

        # populate the empty lists with each portfolios returns,risk and weights
        for single_portfolio in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            profolio = np.dot(returns_daily, weights)
            profolio_return = pd.DataFrame(profolio)
            rank = profolio_return.rank()
            rank_divided_N = rank / len(rank)  # Rank/N
            one_sub_rank_divided_N = 1 - rank_divided_N  # 1-Rank/N
            one_sub_rank_divided_N_power_v_sub_one = one_sub_rank_divided_N ** (V - 1)  # (1-Rank/N)^(V-1)
            mue = profolio_return.mean().tolist()[0]
            x_avg = one_sub_rank_divided_N_power_v_sub_one.mean().tolist()[0]
            profolio_mue = profolio_return - mue
            rank_sub_x_avg = one_sub_rank_divided_N_power_v_sub_one - x_avg
            profolio_mue_mult_rank_x_avg = profolio_mue * rank_sub_x_avg
            summary = profolio_mue_mult_rank_x_avg.sum().tolist()[0] / (len(rank) - 1)
            gini_daily = summary * (-V)
            gini_annual = gini_daily * (254 ** 0.5)
            profolio_annual = ((1 + mue) ** 254) - 1
            # A call to the function we wrote
            sharpe = profolio_annual / gini_annual * 100
            sharpe_ratio.append(sharpe)
            port_profolio_annual.append(profolio_annual)
            port_gini_annual.append(gini_annual * 100)
            stock_weights.append(weights)
        # a dictionary for Returns and Risk values of each portfolio
        portfolio = {'Profolio_annual': profolio_annual,
                     'Gini': port_gini_annual,
                     'Sharpe Ratio': sharpe_ratio}

        # make a nice dataframe of the extended dictionary
        df = pd.DataFrame(portfolio)
        self.plot(df, selected)
        # get better labels for desired arrangement of columns


    @marshal_with(InputSchema)  # marshalling with marshmallow library
    @use_kwargs(InputSchema, location=('query'))
    def get(self, amountToInvest, riskScore):
        volatilityPercentage = 40
        self.gini(volatilityPercentage)
        stokes = [{'BTC': 10000}, {'ETH': 10000}, {'XRP': 10000}, {'LTC': 10000}, {'BCH': 10000}, {'EOS': 10000}]
        response = ResponseApi("GiniWithML", volatilityPercentage, stokes, amountToInvest, datetime.datetime.now())
        return jsonify(response.__str__())
        # return jsonify()
