from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import current_user
from main.forms import TextForm
from flask_login import login_required

from main.models import Sentence, Word
from main.utils import transform, select_sents

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


@bp.get('/next_sent/<word>/<int:n>')
@login_required
def next_sent(word: str, n: int):
    word_in_learning = Word.get(Word.text == word)
    next_sent, number_last_sent = select_sents(word_in_learning, current_user, n)
    return render_template('main/next_sent.html', sent=next_sent, number_last_sent=number_last_sent, n=n, word=word)


@bp.post('/unlearned_word')
@login_required
def update_unlearned_words():
    learned_words = request.form.getlist('word')
    words_int = list(map(int, learned_words))
    for i in words_int:
        Word.update(is_learned=True).where(Word.id == i).execute()
    words = list(Word
                 .select()
                 .where((Word.user == current_user.id) & (Word.is_learned == False))
                 .order_by(Word.frequency.desc()))
    return render_template('main/words.html', words=words, name='learned')


@bp.get('/change_list_words/<name>')
@login_required
def change_list_words(name: str):
    if name == 'learned':
        words = list(Word
                     .select()
                     .where((Word.user == current_user.id) & (Word.is_learned == True))
                     .order_by(Word.frequency.desc()))
        name = 'unlearned'
    else:
        words = list(Word
                     .select()
                     .where((Word.user == current_user.id) & (Word.is_learned == False))
                     .order_by(Word.frequency.desc()))
        name = 'learned'
    return render_template('main/words.html', words=words, name=name)
