import os
import peewee
import datetime

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
database = peewee.SqliteDatabase(PATH("../database.db"))


class Price(peewee.Model):
    '''
        price, date, crawling_times, time
    '''

    price = peewee.CharField()
    date = peewee.DateField()
    crawling_times = peewee.IntegerField()
    time = peewee.TimeField()

    class Meta:
        database = database


#Price().create_table()
