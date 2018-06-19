import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret'
    DB_HOST = '192.168.163.128'
    DB_USER = 'root'
    DB_PASSWD = '1'
    DB_DATABASE = 'testcms'
    ITEMS_PER_PAGE = 10
    JWT_AUTH_URL_RULE = '/api/v1/users/login'

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
