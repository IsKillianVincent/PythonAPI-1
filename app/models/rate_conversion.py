from peewee import Model, ForeignKeyField, DecimalField, TimestampField
from database import db
from models.currencies import Currency
import datetime

class RateConversion(Model):
    source_currency = ForeignKeyField(Currency, backref='source_currency')
    target_currency = ForeignKeyField(Currency, backref='target_currency')
    rate = DecimalField(max_digits=18, decimal_places=8)
    date_added = TimestampField(default=datetime.datetime.now)

    class Meta:
        database = db
        table_name = 'rate_conversions'
