# Standard Library imports

# Core Flask imports
from flask_mail import Mail
from flask_mongoengine import MongoEngine

# Third-party imports

# App imports


# instantiate the extensions
mail = Mail()
db = MongoEngine()


def initialize_mail(app):
    mail.init_app(app)


def initialize_db(app):
    db.init_app(app)






