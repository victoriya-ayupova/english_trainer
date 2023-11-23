from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import current_user
from main.utils import Extractor
from main.forms import TextForm

bp = Blueprint('main', __name__, url_prefix='/main')


@bp.get('/upload')
def upload():
    return render_template('main/upload.html')


@bp.post('/upload')
def upload_post():
    form = TextForm(request.form)
    form.save_sents(current_user)
    form.save_words(current_user)
    flash('Текст загружен')
    return redirect(url_for('main'))

