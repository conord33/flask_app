import os

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    MONGODB_DATABASE = 'flask_api'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

class TestingConfig(BaseConfig):
    TESTING = True
    MONGODB_DATABASE = 'flask_api_test'

config = {
    "development": "app.config.DevelopmentConfig",
    "testing": "app.config.TestingConfig",
    "default": "app.config.DevelopmentConfig"
}

def configure_app(app):
    config_name = os.getenv('FLAKS_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])