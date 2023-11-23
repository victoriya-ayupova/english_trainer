import spacy
import peewee
from collections import Counter

from main.models import Sentence, Word

nlp = spacy.load("en_core_web_sm")


class Extractor:
    def __init__(self, text: str):
        self.doc = nlp(text)

    def extract_sentences(self):
        sentences = []
        for sent in self.doc.sents:
            sentences.append(sent)
        return sentences

    def extract_words(self):
        words = []
        for token in self.doc:
            if token.is_alpha and not token.is_stop and not token.ent_type:
                words.append(token.text)
        return words


def save_sentences(sentences: list, user_id: int):
    sents = ((sent, user_id) for sent in sentences)
    (Sentence
     .insert_many(sents, fields=[Sentence.text, Sentence.user])
     .on_conflict(action='ignore',
                  conflict_target=[Sentence.text, Sentence.user])).execute()


def save_words(words: list, user_id: int):
    words_with_frequency = Counter(words)
    words_for_db = ((word, user_id, frequency, False) for word, frequency in words_with_frequency.items())
    (Word
     .insert_many(words_for_db, fields=[Word.text, Word.user, Word.frequency, Word.is_learned])
     .on_conflict(conflict_target=[Word.text, Word.user],
                  update={Word.frequency: Word.frequency + peewee.EXCLUDED.frequency},
                  )).execute()


# with open('text.txt', 'r') as file:
#     text = file.read()

# ex = Extractor(text)
# sents = ex.extract_sentences()
# words = ex.extract_words()
#
# save_sentences(sents, 4)
# save_words(words, 4)
