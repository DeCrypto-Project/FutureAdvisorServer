from flask_apispec import MethodResource, marshal_with
from flask_restful import Resource
from server.api.myResponses import ResponseSchema
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
import pandas as pd
import numpy as np


class Gini(MethodResource, Resource):
    def get_optimal_portfolio(self):
        selected_prices_value = self.prices_df[self.selected_assets].dropna()
        num_portfolios = 500
        years = len(selected_prices_value) / 253
        starting_value = selected_prices_value.iloc[0, :]
        ending_value = selected_prices_value.iloc[len(selected_prices_value) - 1, :]
        total_period_return = ending_value / starting_value
        annual_returns = (total_period_return ** (1 / years)) - 1
        annual_covariance = selected_prices_value.pct_change().cov() * 253
        port_returns = []
        port_volatility = []
        sharpe_ratio = []
        stock_weights = []
        num_assets = len(self.selected_assets)
        np.random.seed(101)

        for single_portfolio in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            returns = np.dot(weights, annual_returns)
            volatility = np.sqrt(np.dot(weights.T, np.dot(annual_covariance, weights)))
            sharpe = returns / volatility
            sharpe_ratio.append(sharpe)
            port_returns.append(returns * 100)
            port_volatility.append(volatility * 100)
            stock_weights.append(weights)
        portfolio = {'Returns': port_returns,
                     'Volatility': port_volatility,
                     'Sharpe Ratio': sharpe_ratio}
        for counter, symbol in enumerate(self.selected_assets):
            portfolio[symbol] = [Weight[counter] for Weight in stock_weights]
        df = pd.DataFrame(portfolio)
        column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock for stock in self.selected_assets]
        df = df[column_order]
        best_sharpe_portfolio = df.loc[df['Sharpe Ratio'] == df['Sharpe Ratio'].max()]
        sharpe_portfolio = pd.DataFrame(columns=['Ticker', 'Weight'])
        for i in range(len(self.selected_assets)):
            ticker = self.selected_assets[i]
            weight = best_sharpe_portfolio.loc[:, ticker].iloc[0]
            sharpe_portfolio = sharpe_portfolio.append({'Ticker': ticker, 'Weight': weight}, ignore_index=True)
        sharpe_portfolio = sharpe_portfolio.set_index('Ticker')
        return sharpe_portfolio

    # get /checkCurrentWeather
    @marshal_with(ResponseSchema)  # marshalling with marshmallow library
    def get(self):
        # output = self.start(select=['QQQ','LQD','IEI','SPY'], start_year="2020-1-1", end_year="2020-2-2", num_portfolios1=500)
        # return send_file('cover1.png', mimetype='image/gif')
        return self.gini()






