from wtforms import Form, TextAreaField
from main.utils import Extractor, save_sentences, save_words
from main.translator import translate


class TextForm(Form):
    text = TextAreaField('Text')

    def save_text(self, user_id):
        ex = Extractor(self.text.data)
        self.save_sents(user_id, ex)
        self.save_words(user_id, ex)


    def save_sents(self, user_id, ex: Extractor):
        sents = ex.extract_sentences()
        save_sentences(sents, user_id)

    def save_words(self, user_id, ex: Extractor):
        words = ex.extract_words()
        save_words(words, user_id)

