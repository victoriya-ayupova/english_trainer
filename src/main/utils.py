import spacy
import peewee
from collections import Counter

from flask_login import current_user

from auth.models import User
from main.models import Sentence, Word
from main.translator import translate

nlp_en = spacy.load("en_core_web_sm")


class Extractor:
    def __init__(self, text: str):
        self.doc = nlp_en(text)

    def extract_sentences(self):
        sentences = []
        for sent in self.doc.sents:
            sentences.append(sent)
        return sentences

    def extract_words(self):
        words = []
        for token in self.doc:
            if token.is_alpha and not token.is_stop and not token.ent_type:
                words.append(token.text.lower())
        return words


def save_sentences(sentences: list, user_id: int):
    sents = ((sent, user_id, translate(sent)) for sent in sentences)
    (Sentence
     .insert_many(sents, fields=[Sentence.text, Sentence.user, Sentence.translation])
     .on_conflict(action='ignore',
                  conflict_target=[Sentence.text, Sentence.user])).execute()


def save_words(words: list, user_id: int):
    words_with_frequency = Counter(words)
    words_for_db = ((word, user_id, frequency, False, translate(word)) for word, frequency in words_with_frequency.items())
    (Word
     .insert_many(words_for_db, fields=[Word.text, Word.user, Word.frequency, Word.is_learned, Word.translation])
     .on_conflict(conflict_target=[Word.text, Word.user],
                  update={Word.frequency: Word.frequency + peewee.EXCLUDED.frequency},
                  )).execute()


def mask(word: str) -> str:
    return f'<mstrans:dictionary translation=\"{word}\">{word}</mstrans:dictionary>'


def transform(sent: Sentence, word_in_lerning: Word, current_user: User) -> str:
    learned_words = (Word
                     .select()
                     .where((Word.user == current_user.id) & (Word.is_learned == True))
                     .order_by(Word.frequency.desc()))
    learned_words_text = set(learned_word.text for learned_word in learned_words)
    # sent_ru = [token.text for token in nlp_ru(sent.translation)]
    # sent_lemma = [token.lemma_ for token in nlp_ru(sent.translation)]
    # for token in sent_ru:
    #     if token.lemma_ in learned_words_text:
    #         i = sent_ru.index(token)
    #         word_en = Word.select().where(Word.translation == token.lemma_)[0]
    #         sent_ru[i] = word_en.text
    sent_as_list = [token.text for token in nlp_en(sent.text)]
    for word in sent_as_list:
        if word in learned_words_text:
            i = sent_as_list.index(word)
            sent_as_list[i] = mask(word)
    i = sent_as_list.index(word_in_lerning.text)
    sent_as_list[i] = mask(word_in_lerning.text)
    sent_for_translation = ' '.join(sent_as_list)
    return translate(sent_for_translation)


def select_sents(word: Word, current_user: User, n: int):
    sents = (Sentence
             .select()
             .where((Sentence.user == current_user.id)
                    & (Sentence.text.regexp(fr'\y{word.text}\y'))))
    number_last_sent = sents.count() - 1
    sent = sents.limit(1).offset(n)[0]
    next_sent = transform(sent, word, current_user)
    return next_sent, number_last_sent
