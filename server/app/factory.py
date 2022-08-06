from flask import Flask
from configurations import Config


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    from app.extensions import cors
    cors.init_app(app)

    from api.portfolio import api as portfolios_api
    app.register_blueprint(portfolios_api)

    return app