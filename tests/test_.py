from flask import url_for, session
from flask.testing import FlaskClient
from flask_login import current_user
from peewee import Database
import pytest

from src.auth.models import User


@pytest.mark.parametrize(['endpoint'], [
    ['main'],
    ['main.upload'],
])
def test_login_required(client: FlaskClient, db: Database, endpoint: str):
    response = client.get(url_for(endpoint))
    assert response.status_code == 302
    assert response.location.startswith(url_for('auth.login', _external=False))


@pytest.mark.parametrize(['user_data', 'user_id'], [
    [
        {
            'email': 'lena@mail.ru',
            'password': '123456'
        },
        1
    ],
    [
        {
            'email': 'vasya@mail.ru',
            'password': '123456'
        },
        2
    ],
])
def test_login(client: FlaskClient, db: Database, user_data: dict[str, str], user_id: int):
    with client:
        response = client.post(url_for('auth.login'), data=user_data, follow_redirects=True)
        assert 'Неверный пароль' not in response.data.decode()
        assert response.status_code == 200

        assert current_user.is_authenticated
        assert current_user.name != ''

        assert session['_user_id'] == user_id
        assert session['_fresh'] == True

        assert response.request.cookies.get('session')


@pytest.mark.parametrize(['user_data'],
                         [[{'email': 'lena@mail.ru', 'password': '123'}],
                          [{'email': 'lena@mail.ru', 'password': ''}]])
def test_login_incorrect_password(client: FlaskClient, db: Database, user_data: dict):
    response = client.post(url_for('auth.login'), data=user_data)
    assert 'Неверный пароль' in response.data.decode()
    assert response.status_code == 200


def test_login_not_exist(client: FlaskClient, db: Database):
    response = client.post(url_for('auth.login'), data={'email': 'katya@mail.ru', 'password': '123456'})
    assert 'Такого пользователя не существует' in response.data.decode()
    assert response.status_code == 200


@pytest.mark.parametrize(['user_data'],
                         [[{'name': 'Ekaterina',
                            'email': 'katya@mail.ru',
                            'password': '12345678'}]])
def test_register(client: FlaskClient, db: Database, user_data: dict):
    response = client.post(url_for('auth.register'), data=user_data, follow_redirects=True)
    assert response.status_code == 200
    assert len(User.select()) == 3
    user = User.get(User.email == 'katya@mail.ru')
    assert user.name == 'Ekaterina'


@pytest.mark.parametrize(['user_data'],
                         [[{'name': 'Ekaterina',
                            'email': 'lena@mail.ru',
                            'password': '12345678'}]])
def test_register2(client: FlaskClient, db: Database, user_data: dict):
    response = client.post(url_for('auth.register'), data=user_data)
    assert response.status_code == 200
    assert 'уже есть аккаунт' in response.data.decode()
    assert len(User.select()) == 2


@pytest.mark.parametrize(['user_data'],
                         [[{'name': 'Petya',
                            'email': 'petya@mail.ru',
                            'password': '123456'}]])
def test_register3(client: FlaskClient, db: Database, user_data: dict):
    response = client.post(url_for('auth.register'), data=user_data)
    assert response.status_code == 200
    assert len(User.select()) == 2


