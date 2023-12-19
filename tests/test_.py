from flask import Flask, url_for
from flask.testing import FlaskClient
from peewee import Database
import pytest
from werkzeug.security import generate_password_hash

from src.app import create_app, db as _db
from src.auth.models import User
from src.main.models import Word, Sentence


@pytest.fixture()
def db() -> Database:
    models = [User]
    _db.create_tables(models)
    User.create(name='Elena', email='lena@mail.ru', password=generate_password_hash('123456'))
    User.create(name='Vasya', email='vasya@mail.ru', password=generate_password_hash('123456'))
    yield _db
    _db.drop_tables(models)
    _db.close()


@pytest.fixture
def app() -> Flask:
    _app = create_app()
    context = _app.app_context()
    context.push()
    return _app


@pytest.fixture
def client(app) -> FlaskClient:
    return FlaskClient(app)


@pytest.mark.parametrize(['endpoint'], [
    ['main'],
    ['main.upload'],
])
def test_login_required(client: FlaskClient, db: Database, endpoint: str):
    response = client.get(url_for(endpoint))
    assert response.status_code == 302
    assert response.location.startswith(url_for('auth.login', _external=False))


@pytest.mark.parametrize(['user_data'], [
    [{
        'email': 'lena@mail.ru',
        'password': '123456'
    }],
    [{
        'email': 'vasya@mail.ru',
        'password': '123456'
    }],
])
def test_login(client: FlaskClient, db: Database, user_data: dict[str, str]):
    response = client.post(url_for('auth.login'), data=user_data)
    assert 'Неверный пароль' not in response.data.decode()
    assert response.status_code == 302
    assert response.location.startswith(url_for('main', _external=False))
