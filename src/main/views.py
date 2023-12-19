from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import current_user
from main.forms import TextForm
from flask_login import login_required

from main.models import Sentence
from main.utils import transform

bp = Blueprint('main', __name__, url_prefix='/main')


@bp.get('/upload')
@login_required
def upload():
    form = TextForm()
    return render_template('main/upload.html', form=form)


@bp.post('/upload')
@login_required
def upload_post():
    form = TextForm(request.form)
    form.save_text(current_user)
    flash('Текст загружен')
    return redirect(url_for('main'))


@bp.post('/next_sent')
@login_required
def next_sent():
    form = request.form
    word = form['word']
    n = int(form['sent_number'])
    sents = (Sentence
             .select()
             .where((Sentence.user == current_user.id)
                    & (Sentence.text.like(f'%{word}%'))))
    number_last_sent = sents.count() - 1
    sent = sents.limit(1).offset(n)[0]
    next_sent = transform(sent.text, word)
    return render_template('main/next_sent.html', sent=next_sent, number_last_sent=number_last_sent, n=n, word=word)