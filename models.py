import datetime
from peewee import *

DATABASE = SqliteDatabase("grow.db")

class Book(Model):
    title = TextField()
    image = TextField()
    author = TextField()
    ISBN_10 = TextField()
    current_page = IntegerField()
    total_pages = IntegerField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Book], safe=True)
    DATABASE.close()