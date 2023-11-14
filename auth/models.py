from peewee import Model, CharField, PostgresqlDatabase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = PostgresqlDatabase('english_trainer', **{'port': 5433, 'user': 'postgres', 'password': 'Televizor%1996'})


class BaseModel(Model):
    class Meta:
        database = db


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
