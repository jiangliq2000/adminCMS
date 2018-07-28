import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret'
    DB_HOST = '192.168.163.128'
    DB_USER = 'root'
    DB_PASSWD = '1'
    DB_DATABASE = 'test'
    ITEMS_PER_PAGE = 10
    JWT_AUTH_URL_RULE = '/api/v1/users/login'
    JWT_EXPIRATION_DELTA = timedelta(days=1)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    PRODUCTION = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
