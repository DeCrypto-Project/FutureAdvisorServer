# import datetime
#
# from app.extensions import db
# from models.enums.algorithm import Algorithm
# from sqlalchemy.orm import relationship
#
#
# class Portfolio(db.Model):
#
#     __tablename__ = 'portfolios'
#
#     id = db.Column('id', db.Integer, nullable=False, primary_key=True, autoincrement=True)
#     date_time = db.Column('date_time', db.DateTime, default=datetime.datetime.now)
#     algorithm = db.Column('algorithm', db.String)
#     risk = db.Column('risk',  db.Integer)
#     link = db.Column('link', db.String)
#     port_user_answers_set = relationship("PortUserAnswersSet", backref='portfolio')
#     portfolio_stocks = relationship("PortfolioStocks", backref='portfolio')
#
#     def as_dict(self):
#         portfolio_as_dict = {
#             'date_time': self.date_time.strftime('%m-%d-%Y'),
#             'algorithm': self.algorithm,
#             'risk': self.risk,
#             'link': self.link
#         }
#         return portfolio_as_dict