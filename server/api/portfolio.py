from flask import Blueprint
from flask.views import MethodView
from app.configurations import Config


class PortfolioApi(MethodView):

    def get(self):
        return "hello world"


api = Blueprint('portfolio_api', __name__, url_prefix=Config.API_PREFIX + '/portfolios')
portfolios = PortfolioApi.as_view('api_portfolio')
api.add_url_rule('/get_portfolio', methods=['GET'], view_func=portfolios)
