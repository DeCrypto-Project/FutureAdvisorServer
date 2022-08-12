from flask import Flask
import flask_restful
import redis as redis
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec import FlaskApiSpec
from flask_cors import CORS

from server.api.gini import Gini

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config[
    'PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on server
api = flask_restful.Api(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Future Advisor Server ',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0',

    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
cache = redis.Redis(host='redis', port=6379)
api.add_resource(Gini, '/gini')
docs = FlaskApiSpec(app)
docs.register(Gini)


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Expose-Headers', 'Content-Type,Content-Length,Authorization,X-Pagination')
    return response