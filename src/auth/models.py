from peewee import CharField
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from db import BaseModel


class User(BaseModel, UserMixin):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

    def change_password(self, new_password):
        hashed_password = generate_password_hash(new_password)
        self.password = hashed_password
        self.save()

    class Meta:
        table_name = 'users'
