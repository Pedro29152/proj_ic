# -*- coding: utf-8 -*-

# Python
import os
from os import getenv

class Config:
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    STATIC_FOLDER = os.path.join(APP_ROOT, 'static')
    SLIDES_FOLDER = os.path.join(APP_ROOT, 'static', 'slides')
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'files')
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024
    PROPAGATE_EXCEPTIONS = True

    SECRET_KEY = getenv('SECRET_KEY')
    APP_PORT = int(getenv('APP_PORT'))
    DEBUG = eval(getenv('DEBUG').title())
    SEND_EMAILS = eval(getenv('SEND_EMAILS').title())

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True

class TestingConfig(Config):
    FLASK_ENV = 'testing'
    TESTING = True

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
