import flask_restful
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_cors import CORS
from flask_apispec import FlaskApiSpec

from server.api.portfolioApi import DriveStatus
from server.api.wheather import Weather

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on server
api = flask_restful.Api(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='futre ',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0',


    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})


#api.add_resource(Auth, '/v1/api/auth')
api.add_resource(Weather, '/')
#api.add_resource(PortfolioApi, '/v1/api/driveStatus')
docs = FlaskApiSpec(app)
docs.register(Weather)
#docs.register(PortfolioApi)
#docs.register(Auth)


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Expose-Headers', 'Content-Type,Content-Length,Authorization,X-Pagination')
    return response



if __name__ == '__main__':
    app.run(port=5000, debug=True)
