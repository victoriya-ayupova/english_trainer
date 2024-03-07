import pytest
from flask import Flask
from flask.testing import FlaskClient
from peewee import Database
from werkzeug.security import generate_password_hash

from app import create_app
from auth.models import User
from db import db as _db
from main.models import Word, Sentence


@pytest.fixture()
def db(app) -> Database:
    models = [User, Word, Sentence]
    _db.drop_tables(models)
    _db.create_tables(models)
    User.create(name='Elena', email='lena@mail.ru', password=generate_password_hash('123456'))
    User.create(name='Vasya', email='vasya@mail.ru', password=generate_password_hash('123456'))
    yield _db
    _db.drop_tables(models)
    _db.close()


@pytest.fixture
def app() -> Flask:
    _app = create_app('../test')
    context = _app.app_context()
    context.push()
    return _app


@pytest.fixture
def client(app) -> FlaskClient:
    return FlaskClient(app)


@pytest.fixture
def authentication_credentials():
    return {
        'name': ...,
    }
