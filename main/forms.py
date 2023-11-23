from wtforms import Form, StringField
from main.utils import Extractor, save_sentences, save_words


class TextForm(Form):
    text = StringField('Text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ex = Extractor(self.text.data)

    def save_sents(self, user_id):
        sents = self.ex.extract_sentences()
        save_sentences(sents, user_id)

    def save_words(self, user_id):
        words = self.ex.extract_words()
        save_words(words, user_id)