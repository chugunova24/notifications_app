# Standard Library imports
from flask import Blueprint
from flask_restful import Api

# Core Flask imports

# Third-party imports

# App imports
from .views import (users_views,
                    notifications_views)

main_bp = Blueprint('main', __name__)
api = Api(main_bp)


def initialize_bp(app):
    main_bp.register_blueprint(notifications_views.notifications_bp)

    app.register_blueprint(main_bp)


def initialize_routes(app):
    initialize_bp(app)
    api.add_resource(users_views.UserView, '/register')



