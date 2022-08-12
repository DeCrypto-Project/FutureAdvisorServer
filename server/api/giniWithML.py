from flask import jsonify
from flask_apispec import MethodResource, marshal_with, use_kwargs
from flask_restful import Resource
from server.api.myResponses import InputSchema
import matplotlib.pyplot as plt

from server.dto.responseApi import ResponseApi

#plt.switch_backend('Agg')
import yfinance as yf
import math
import numpy as np
import pandas as pd
import datetime
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from pandas_datareader import data as pdr


class GiniWithML(MethodResource, Resource):

    def gini(self, selected,volatile, start_year, end_year):
        # Select stocks, start year and end year, stock number has no known limit
        Num_porSimulation = 100
        V = volatile

        # Building the dataframe
        yf.pdr_override()
        frame = {}
        for stock in selected:
            data_var = pdr.get_data_yahoo(stock, start_year, end_year)['Adj Close']
            #data_var = yf.download(stock, start_year, end_year)['Adj Close']
            data_var.to_frame()
            frame.update({stock: data_var})

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
            profolio_annual_new = self.analyzeMechainLearningFunc(profolio_return, table.index)
            sharpe = profolio_annual_new / gini_annual * 100
            sharpe_ratio.append(sharpe)
            port_profolio_annual.append(profolio_annual_new)
            port_gini_annual.append(gini_annual * 100)
            stock_weights.append(weights)

        # a dictionary for Returns and Risk values of each portfolio
        portfolio = {'Profolio_annual': port_profolio_annual,
                     'Gini': port_gini_annual,
                     'Sharpe Ratio': sharpe_ratio}

        # extend original dictionary to accomodate each ticker and weight in the portfolio
        for counter, symbol in enumerate(selected):
            portfolio[symbol + ' Weight'] = [Weight[counter] for Weight in stock_weights]

        # make a nice dataframe of the extended dictionary
        df = pd.DataFrame(portfolio)

        # get better labels for desired arrangement of columns
        column_order = ['Profolio_annual', 'Gini', 'Sharpe Ratio'] + [stock + ' Weight' for stock in selected]

        # reorder dataframe columns
        df = df[column_order]
        self.plot(df, selected)

    def plot(self, df, selected):
        # plot frontier, max sharpe & min Gini values with a scatterplot
        # find min Gini & max sharpe values in the dataframe (df)
        min_gini = df['Gini'].min()
        max_sharpe = df['Sharpe Ratio'].max()
        max_profolio_annual = df['Profolio_annual'].max()
        max_gini = df['Gini'].max()

        # use the min, max values to locate and create the two special portfolios
        sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
        min_variance_port = df.loc[df['Gini'] == min_gini]
        max_profolios_annual = df.loc[df['Profolio_annual'] == max_profolio_annual]
        max_ginis = df.loc[df['Gini'] == max_gini]

        # plot frontier, max sharpe & min Gini values with a scatterplot
        plt.style.use('seaborn-dark')
        df.plot.scatter(x='Gini', y='Profolio_annual', c='Sharpe Ratio',
                        cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
        plt.scatter(x=sharpe_portfolio['Gini'], y=sharpe_portfolio['Profolio_annual'], c='green', marker='D', s=200)
        plt.scatter(x=min_variance_port['Gini'], y=min_variance_port['Profolio_annual'], c='orange', marker='D', s=200)
        plt.scatter(x=max_ginis['Gini'], y=max_profolios_annual['Profolio_annual'], c='red', marker='D', s=200)
        plt.style.use('seaborn-dark')

        plt.xlabel('Gini (Std. Deviation) Percentage %')
        plt.ylabel('Expected profolio annual Percentage %')
        plt.title('Efficient Frontier')
        plt.subplots_adjust(bottom=0.4)

        # ------------------ Pritning 3 optimal Protfolios -----------------------
        # Setting max_X, max_Y to act as relative border for window size

        red_num = df.index[df["Profolio_annual"] == max_profolio_annual]
        yellow_num = df.index[df['Gini'] == min_gini]
        green_num = df.index[df['Sharpe Ratio'] == max_sharpe]
        multseries = pd.Series([1, 1, 1] + [100 for stock in selected],
                               index=['Profolio_annual', 'Gini', 'Sharpe Ratio'] + [stock + ' Weight' for stock in
                                                                                    selected])
        with pd.option_context('display.float_format', '%{:,.2f}'.format):
            plt.figtext(0.2, 0.15,
                        "Max Profolio_annual Porfolio: \n" + df.loc[red_num[0]].multiply(multseries).to_string(),
                        bbox=dict(facecolor='red', alpha=0.5), fontsize=11, style='oblique', ha='center', va='center',
                        wrap=True)
            plt.figtext(0.45, 0.15, "Safest Portfolio: \n" + df.loc[yellow_num[0]].multiply(multseries).to_string(),
                        bbox=dict(facecolor='yellow', alpha=0.5), fontsize=11, style='oblique', ha='center',
                        va='center', wrap=True)
            plt.figtext(0.7, 0.15, "Sharpe  Portfolio: \n" + df.loc[green_num[0]].multiply(multseries).to_string(),
                        bbox=dict(facecolor='green', alpha=0.5), fontsize=11, style='oblique', ha='center', va='center',
                        wrap=True)
        plt.savefig("plot_gini_with_ml.png")

    def analyzeMechainLearningFunc(self, profolio_return, table_index):
        df_final = pd.DataFrame({})
        forecast_col = 'col'
        df_final[forecast_col] = profolio_return
        # forecast_col= 'ADJ_PCT_change_SPY'
        df_final.fillna(value=-0, inplace=True)
        forecast_out = int(math.ceil(0.01 * len(df_final)))
        df_final['label'] = df_final[forecast_col].shift(-forecast_out)
        # print(df_final.head())
        # df_final.to_csv('Out.csv')

        # Added date
        df = df_final
        df['Date'] = table_index
        # print(df)
        X = np.array(df.drop(['label', 'Date'], 1))
        X = preprocessing.scale(X)
        X_lately = X[-forecast_out:]
        X = X[:-forecast_out]
        df.dropna(inplace=True)

        y = np.array(df['label'])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
        clf = LinearRegression()
        clf.fit(X_train, y_train)
        confidence = clf.score(X_test, y_test)
        print(confidence)
        forecast_set = clf.predict(X_lately)
        df['Forecast'] = np.nan

        last_date = df.iloc[-1]['Date']
        last_unix = last_date.timestamp()
        one_day = 86400
        next_unix = last_unix + one_day

        for i in forecast_set:
            next_date = datetime.datetime.fromtimestamp(next_unix)
            next_unix += 86400
            df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1)] + [i]

        df['Forecast'].plot()
        # df['Forecast'].to_csv('Out-f.csv')

        ans = (((1 + df['Forecast'].mean()) ** 254) - 1) * 100
        print(ans)
        return ans

    @marshal_with(InputSchema)  # marshalling with marshmallow library
    @use_kwargs(InputSchema, location=('query'))
    def get(self, amountToInvest, riskScore):
        volatilityPercentage = 40
        #stocks = [{'BTC': 10000}, {'ETH': 10000}, {'XRP': 10000}, {'LTC': 10000}, {'BCH': 10000}, {'EOS': 10000}]
        #stocks = ["SPY","IEI","LQD","QQQ"]
        stocks = ["BTC-USD","ETH-USD", "ADA-USD"]
        start_date = '2019-01-01'
        end_date = '2019-01-10'
        gini_res = self.gini(stocks, volatilityPercentage, start_date, end_date)
        response = ResponseApi("GiniWithML", volatilityPercentage, stocks, amountToInvest, datetime.datetime.now())
        return jsonify(response.__str__())
        # return jsonify()