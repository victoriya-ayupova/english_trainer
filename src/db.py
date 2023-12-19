from peewee import PostgresqlDatabase, Model

db = PostgresqlDatabase(None)
# db = PostgresqlDatabase('english_trainer', **{'port': 5433, 'user': 'postgres', 'password': 'Televizor%1996'})


class BaseModel(Model):
    class Meta:
        database = db
