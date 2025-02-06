from peewee import Model, CharField
from database import db

class Currency(Model):
    code = CharField(unique=True)
    name = CharField()

    class Meta:
        database = db
        table_name = 'currencies'

    def __str__(self):
        return self.code
