# from sqlalchemy.orm import relationship
#
# from app.extensions import db
# from models.enums.algorithm import Algorithm
#
#
# class PortfolioStocks(db.Model):
#     __tablename__ = 'portfolio_stocks'
#
#     stock_price_ticker = db.Column(db.String, primary_key=True)
#     stock_price_date_time = db.Column(db.DateTime)
#     portfolios_id = db.Column(db.Integer, primary_key=True)
#     weight = db.Column(db.Numeric)
#
#     __table_args__ = (
#         db.ForeignKeyConstraint(
#             ['stock_price_ticker', 'stock_price_date_time'],
#             ['stocks_prices.ticker', 'stocks_prices.date_time'],
#         ),
#         db.ForeignKeyConstraint(
#             ['portfolios_id'],
#             ['portfolios.id'],
#         ),
#     )
#
#     def as_dict(self):
#         portfolio_stock_as_dict = {
#             'stock_price_ticker': self.stock_price_ticker,
#             'stock_price_date_time': self.stock_price_date_time,
#             'weight': str(self.weight.real),
#             'asset_type': self.stock_price.asset_type # stock_price is backref from StockPrice model
#         }
#         return portfolio_stock_as_dict