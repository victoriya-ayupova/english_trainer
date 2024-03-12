import logging
import os

import spacy
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_required
from loguru import logger
from dotenv import dotenv_values

from auth.models import User
from auth.views import bp as auth_bp
from main.models import Word, Sentence
from main.translator import translate
from main.utils import transform, select_sents
from main.views import bp as main_bp
from db import db

logger.add('app.log', level=logging.DEBUG)


@login_required
def main():
    words = list(Word
                 .select()
                 .where((Word.user == current_user.id) & (Word.is_learned == False))
                 .order_by(Word.frequency.desc()))

    try:
        word = words[0].text.lower()
    except IndexError:
        word = None
    n = int(request.args.get('n', 0))
    if word is not None:
        ready_sent, number_last_sent = select_sents(words[0], current_user, n)
    else:
        ready_sent = 'У вас нет слов для изучения. Загрузите текст'
        number_last_sent = 0
    return render_template('main/main.html', words=words, sent=ready_sent,
                           n=n, number_last_sent=number_last_sent, word=word, name='learned')


@login_required
def main_post():
    form = request.form
    button = form['type']

    if button == 'Вперед':
        new_sent_number = int(form['sent_number'])
    else:
        new_sent_number = int(form['sent_number'])
    return redirect(url_for('main', n=new_sent_number))


# /word/123/456
# from urllib.parse import urljoin
# urljoin(url_for('word'), '.../...')
# @app.get('/word/<int:word_id>/<int:sentence_id>')
# def word(word_id: int, sentence_id: int) -> str:
#     words = ...
#     sentence = ...
#     return render_template(...)


def error404(error):
    return render_template('errors/404.html')


def user_load(id: str):
    return User.get_by_id(int(id))


def create_app(config_name: str):
    app = Flask(__name__)
    logger.debug('App created')
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.add_url_rule('/', view_func=main)
    app.add_url_rule('/', methods=['POST'], view_func=main_post)
    app.register_error_handler(404, error404)
    logger.debug('App configuration finished')

    config = dotenv_values(f'{config_name}.env')
    if not config:
        raise RuntimeError(f'Unable to load {config_name}.env')
    logger.debug('Environment created')
    app.config.update(config)
    db.init(
        app.config['DB_NAME'],
        host=app.config['DB_HOST'],
        port=app.config['DB_PORT'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
    )
    logger.debug('Database initialized')

    # app.secret_key = os.environ.get('FLASK_SECRET_KEY')
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(user_load)
    login_manager.login_view = 'auth.login'
    logger.debug('Login manager initialized')

    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run(port=5001)
