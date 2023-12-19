import os

import spacy
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_required

from auth.models import User
from auth.views import bp as auth_bp
from config import DevelopmentConfig, TestConfig
from main.models import Word, Sentence
from main.utils import transform
from main.views import bp as main_bp
from db import db
nlp = spacy.load("en_core_web_sm")


@login_required
def main():
    words = list(Word
                 .select()
                 .where((Word.user == current_user.id) & (Word.is_learned == False))
                 .order_by(Word.frequency.desc()))[:15]
    word = words[0].text.lower()
    try:
        n = int(request.args['n'])
    except Exception:
        n = 0
    sents = (Sentence
             .select()
             .where((Sentence.user == current_user.id)
                    & (Sentence.text.like(f'%{word}%'))))
    number_last_sent = sents.count() - 1
    sent = sents.limit(1).offset(n)[0]
    sent_translated = transform(sent.text, word)
    return render_template('main/main.html', words=words, sent=sent_translated,
                           n=n, number_last_sent=number_last_sent, word=word)


@login_required
def main_post():
    form = request.form
    button = form['type']

    if button == 'Вперед':
        new_sent_number = int(form['sent_number'])
    else:
        new_sent_number = int(form['sent_number'])
    return redirect(url_for('main', n=new_sent_number))


def error404(error):
    return render_template('errors/404.html')


def user_load(id: str):
    return User.get_by_id(int(id))


def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.add_url_rule('/', view_func=main)
    app.add_url_rule('/', methods=['POST'], view_func=main_post)
    app.register_error_handler(404, error404)

    config_map = {
        'development': DevelopmentConfig,
        'test': TestConfig,
    }
    config = config_map[os.environ.get('FLASK_ENV', 'development')]
    app.config.from_object(config)
    db.init(
        config.DB_NAME,
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )

    # app.secret_key = os.environ.get('FLASK_SECRET_KEY')
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(user_load)
    login_manager.login_view = 'auth.login'

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5001)
