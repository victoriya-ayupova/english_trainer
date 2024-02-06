import peewee
from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from .forms import LoginForm, RegisterForm, PasswordRecoveryForm
from .models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.get('/login')
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@bp.post('/login')
def login_post():
    form = LoginForm(request.form)
    if not form.validate():
        return render_template('auth/login.html', form=form)

    user = User.get(User.email == form.email.data)
    login_user(user)
    if request.args.get('next') is not None:
        return redirect(request.args.get('next'))
    else:
        return redirect(url_for('main'))


@bp.get('/register')
def register():
    form = RegisterForm()
    return render_template('auth/register.html', form=form)


@bp.post('/register')
def register_post():
    form = RegisterForm(request.form)
    if not form.validate():
        return render_template('auth/register.html', form=form)

    user = User.create(
        name=form.name.data,
        email=form.email.data,
        password=generate_password_hash(form.password.data)
    )
    login_user(user)
    return redirect(url_for('main'))


@bp.get('/password_recovery')
def recovery():
    form = PasswordRecoveryForm(request.form)
    return render_template('auth/password_recovery.html', form=form)


@bp.post('/password_recovery')
def recovery_post():
    form = PasswordRecoveryForm(request.form)
    if not form.validate():
        return render_template('auth/password_recovery.html', form=form)
    user = User.get(User.email == form.email.data)
    user.change_password(form.password.data)
    flash('Пароль обновлен')
    return redirect(url_for('auth.login'))


@bp.get('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
