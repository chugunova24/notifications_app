# Standard Library imports
import os

# Core Flask imports

# Third-party imports
from dotenv import dotenv_values

# App imports


env_file = os.path.join(os.path.dirname(__file__), ".env")
# basedir = os.path.abspath(os.path.dirname(__file__))
# env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')
environs = dotenv_values(env_file)

print(f"Environs: {environs}")


class Config:
    # base
    SECRET_KEY = environs.get("FLASK_SECRET_KEY")
    DEBUG = False
    MAX_SIZE_NOTIFICATIONS = int(environs.get('FLASK_MAX_SIZE_NOTIFICATIONS'))
    FLASK_TEST_NOTIFICATIONS = environs.get('FLASK_TEST_NOTIFICATIONS')

    # mongodb database
    MONGODB_SETTINGS = {
        "db": environs.get('MONGO_DB'),
        'username': environs.get('MONGO_USERNAME'),
        'password': environs.get('MONGO_PASSWORD'),
        'host': environs.get('MONGO_HOST'),
        'port': int(environs.get('MONGO_PORT'))
    }

    # email server
    MAIL_SERVER = environs.get('MAIL_SERVER')
    MAIL_PORT = int(environs.get('MAIL_PORT'))
    MAIL_USE_TLS = environs.get('MAIL_USE_TLS')
    MAIL_USE_SSL = environs.get('MAIL_USE_SSL')
    MAIL_USERNAME = environs.get('MAIL_USERNAME')
    MAIL_PASSWORD = environs.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # Configure the redis server
    REDIS_HOST = environs.get('REDIS_HOST')
    REDIS_PORT = environs.get('REDIS_PORT')
    REDIS_DB = int(environs.get('REDIS_DB'))
    BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
    RESULT_BACKEND = BROKER_URL

    # Configure the celery
    CELERY = dict(
        broker_url=BROKER_URL,
        result_backend=RESULT_BACKEND,
        include=['app.tasks']
    )


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False


config_manager = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
