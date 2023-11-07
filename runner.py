# Standard Library imports

# Core Flask imports

# Third-party imports

# App imports
from app import create_app
from config import environs


app, ext_celery = create_app(environs.get('FLASK_CONFIG', None) or "dev")
celery = ext_celery.celery
