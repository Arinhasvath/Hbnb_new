class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'dev'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True