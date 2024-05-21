"""
    Archive have a method to start a flask application with yours configs
"""
import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()


def create_app():
    """
    All flask app settings are in this method
    :return: app
    """
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # loading configs
    app.config.from_object(Config)

    # instances
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    blueprint = Blueprint('api', __name__)
    app.register_blueprint(blueprint)

    authorizations = {
        'apiKey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorizations',
            'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
        }
    }

    api = Api(app,
              title="API Antiquário",
              version="0.1",
              description="Initial antique API",
              prefix="/api",
              authorizations=authorizations,
              security='apiKey')

    from app import resources
    resources.init_app(api)

    return app
