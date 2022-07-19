# from flask import Flask
# from .configurations import Config
# from flask import Flask
#
# from .configurations import Config
# from .extensions import db
#
#
# def create_app():
#     app = Flask(__name__)
#
#     app.config.from_object(Config)
#
#     from app.extensions import cors
#     cors.init_app(app)
#     # Set up database
#     db.init_app(app)
#
#     from api.users_api import api as users_api
#     from api.members_api import api as members_api
#     from api.portfolio_api import api as portfolio_api
#     from api.clusters_api import api as clusters_api
#     from api.topics_api import api as topics_api
#     from api.messages_api import api as messages_api
#     from api.form_submit import api as submit_form_api
#     from api.reset_password import api as reset_password_api
#     from api.recent_results_api import api as recent_results_api
#     from api.articles_api import api as articles_api
#     from api.rebalance_api import api as rebalance_api
#
#     app.register_blueprint(users_api)
#     app.register_blueprint(members_api)
#     app.register_blueprint(portfolio_api)
#     app.register_blueprint(clusters_api)
#     app.register_blueprint(topics_api)
#     app.register_blueprint(messages_api)
#     app.register_blueprint(submit_form_api)
#     app.register_blueprint(reset_password_api)
#     app.register_blueprint(recent_results_api)
#     app.register_blueprint(rebalance_api)
#     app.register_blueprint(articles_api)
#
#     # Create tables
#     with app.app_context():
#         db.create_all()
#         return app