import os

from flask import Flask, render_template, request
from flask_login import login_user, login_required, LoginManager, current_user

from auth.models import User
from auth.views import bp as auth_bp
from main.views import bp as main_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

app.secret_key = 'asdf'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def user_load(id: str):
    return User.get_by_id(int(id))


@app.get('/')
def main():
    return render_template('main/main.html')


@app.errorhandler(404)
def error404(error):
    return render_template('errors/404.html')


@app.get('/env')
def show_env():
    return os.environ['TEST1']


@app.get('/profile')
def profile():
    return None


app.run()
