import os
from pathlib import Path

from dotenv import dotenv_values


class Config:
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']
    DB_NAME = os.environ['DB_NAME']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ['DB_PORT']
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']


class DevelopmentConfig(Config):
    TESTING = False
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    DEBUG = False
    SERVER_NAME = os.environ.get('SERVER_NAME')

