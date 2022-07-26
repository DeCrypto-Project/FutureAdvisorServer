from flask_apispec import MethodResource, marshal_with
from flask_restful import Resource
from myResponses import ResponseSchemaWeather
from pandas_datareader import data as pdr
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
import pandas as pd
from flask import send_file

class Weather(MethodResource, Resource):

    num_portfolios = 500
    selected = []

    def start(self, select, start_year, end_year, num_portfolios1):
        global selected
        global num_portfolios
        num_portfolios = num_portfolios1
        selected = select
        yf.pdr_override()
        frame = {}
        for stock in selected:
            data_var = pdr.get_data_yahoo(stock, start_year, end_year)['Adj Close']
            data_var.to_frame()
            frame.update({stock: data_var})
            table = pd.DataFrame(frame)
        self.create_portfolios(table)

    def create_portfolios(self, table):
        returns_daily = table.pct_change()
        returns_annual = ((1 + returns_daily.mean()) ** 250) - 1
        cov_daily = returns_daily.cov()
        cov_annual = cov_daily * 250
        port_returns = []
        port_volatility = []
        sharpe_ratio = []
        stock_weights = []
        num_assets = len(selected)
        np.random.seed(101)

        for single_portfolio in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            returns = np.dot(weights, returns_annual)
            volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
            sharpe = returns / volatility
            sharpe_ratio.append(sharpe)
            port_returns.append(returns * 100)
            port_volatility.append(volatility * 100)
            stock_weights.append(weights)
        portfolio = {'Returns': port_returns,
                     'Volatility': port_volatility,
                     'Sharpe Ratio': sharpe_ratio}
        for counter, symbol in enumerate(selected):
            portfolio[symbol + ' Weight'] = [Weight[counter] for Weight in stock_weights]
        df = pd.DataFrame(portfolio)
        column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock + ' Weight' for stock in selected]
        df = df[column_order]
        self.plot_portfolios(df)

    def plot_portfolios(self, df):
        min_volatility = df['Volatility'].min()
        max_sharpe = df['Sharpe Ratio'].max()
        max_return = df['Returns'].max()
        max_vol = df['Volatility'].max()
        sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
        min_variance_port = df.loc[df['Volatility'] == min_volatility]
        max_returns = df.loc[df['Returns'] == max_return]
        max_vols = df.loc[df['Volatility'] == max_vol]
        plt.style.use('seaborn-dark')
        df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                        cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
        plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='green', marker='D', s=200)
        plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='orange', marker='D', s=200)
        plt.scatter(x=max_vols['Volatility'], y=max_returns['Returns'], c='red', marker='D', s=200)
        plt.style.use('seaborn-dark')
        plt.xlabel('Volatility (Std. Deviation) Percentage %')
        plt.ylabel('Expected Returns Percentage %')
        plt.title('Efficient Frontier')
        plt.subplots_adjust(bottom=0.4)
        red_num = df.index[df["Returns"] == max_return]
        yellow_num = df.index[df['Volatility'] == min_volatility]
        green_num = df.index[df['Sharpe Ratio'] == max_sharpe]
        multseries = pd.Series([1, 1, 1] + [100 for stock in selected],
                               index=['Returns', 'Volatility', 'Sharpe Ratio'] + [stock + ' Weight' for stock in
                                                                                  selected])
        with pd.option_context('display.float_format', '%{:,.2f}'.format):
            plt.figtext(0.2, 0.15, "Max returns Porfolio: \n" + df.loc[red_num[0]].multiply(multseries).to_string(),
                        bbox=dict(facecolor='red', alpha=0.5), fontsize=11, style='oblique', ha='center', va='center',
                        wrap=True)
            plt.figtext(0.45, 0.15, "Safest Portfolio: \n" + df.loc[yellow_num[0]].multiply(multseries).to_string(),
                        bbox=dict(facecolor='yellow', alpha=0.5), fontsize=11, style='oblique', ha='center',
                        va='center', wrap=True)
            plt.figtext(0.7, 0.15, "Sharpe  Portfolio: \n" + df.loc[green_num[0]].multiply(multseries).to_string(),
                        bbox=dict(facecolor='green', alpha=0.5), fontsize=11, style='oblique', ha='center', va='center',
                        wrap=True)
        self.save_plot(plt)

    def save_plot(self, plt):
        plt.savefig('static/cover1.png')
        return ("Saved")

    # get /checkCurrentWeather
    @marshal_with(ResponseSchemaWeather)  # marshalling with marshmallow library
    def get(self):

        output = self.start(select=['QQQ','LQD','IEI','SPY'], start_year="2020-1-1", end_year="2020-2-2", num_portfolios1=500)
        return send_file('cover1.png', mimetype='image/gif')






