from peewee import CharField, IntegerField, BooleanField, ForeignKeyField, SQL
from db import BaseModel
from auth.models import User


class Sentence(BaseModel):
    text = CharField()
    user = ForeignKeyField(User)

    class Meta:
        constraints = [SQL('UNIQUE (text, user_id)')]


class Word(BaseModel):
    text = CharField()
    user = ForeignKeyField(User)
    frequency = IntegerField()
    is_learned = BooleanField()

    class Meta:
        constraints = [SQL('UNIQUE (text, user_id)')]

