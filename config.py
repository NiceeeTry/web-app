from datetime import timedelta
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    FLASK_ADMIN_SWATCH = 'cerulean'
    
class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY ='super-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:qwerty@localhost:5432/flask_db'
    
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI ='postgresql://postgres:qwerty@localhost:5432/test'
    SQLALCHEMY_ECHO=False
    SECRET_KEY ='super-secret-key'
    TESTING=True