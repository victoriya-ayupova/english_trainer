from peewee import CharField, IntegerField, BooleanField, ForeignKeyField, SQL
from db import BaseModel
from auth.models import User


class Sentence(BaseModel):
    text = CharField()
    user = ForeignKeyField(User)
    translation = CharField()

    class Meta:
        table_name = 'sentence'
        constraints = [SQL('UNIQUE (text, user_id)')]


class Word(BaseModel):
    text = CharField()
    user = ForeignKeyField(User)
    frequency = IntegerField()
    is_learned = BooleanField()
    translation = CharField()

    class Meta:
        table_name = 'word'
        constraints = [SQL('UNIQUE (text, user_id)')]

