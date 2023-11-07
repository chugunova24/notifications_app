# Standard Library imports

# Core Flask imports
from flask import Flask
from flask_celeryext import FlaskCeleryExt

# Third-party imports

# App imports
from config import config_manager
from app.utils.utils import MongoJSONEncoder
from .extensions import (initialize_mail, initialize_db)
from .routes import initialize_routes, initialize_bp, api
from .celery_utils import make_celery


ext_celery = FlaskCeleryExt(create_celery_app=make_celery)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_manager[config_name])

    app.json_encoder = MongoJSONEncoder
    app.json.sort_keys = False

    ext_celery.init_app(app)

    initialize_mail(app)
    initialize_db(app)
    initialize_routes(app)

    return app, ext_celery
