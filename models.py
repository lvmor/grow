import datetime
from peewee import *

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase("grow.db")
# pg_db = PostgresqlDatabase('grow', user='postgres', password='secret',
#                            host='127.0.0.1', port=5432)

class User(UserMixin, Model):
    name = CharField()
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField(max_length=15)
    avatar = CharField()
    genre = CharField()

    class Meta:
        database = DATABASE
    
    @classmethod
    def create_user(cls, name, username, email, password, avatar, genre):
        cls.create(
                name = name,
                username = username,
                email = email,
                password = generate_password_hash(password),
                avatar = avatar,
                genre = genre
            )
        
        # try:
            
        # except IntegrityError:
        #     raise ValueError("User/Email already exists")
class Book(Model):
    # timestamp = DateTimeField(default=datetime.datetime.now)
    title = TextField()
    image = TextField()
    author = TextField()
    ISBN_13 = TextField()
    ISBN_10 = TextField()
    date_published = TextField()
    description = TextField()
    total_pages = IntegerField()

    class Meta:
        database = DATABASE
        # order_by = ('-timestamp',)

class Goal(Model):
    # timestamp = DateTimeField(default=datetime.datetime.now)
    user_id = ForeignKeyField(model=User, backref="user")
    book_id = ForeignKeyField(model=Book, backref="book")
    start_date = TextField()
    end_date = TextField()
    book_progress = IntegerField()
    status = TextField()
    notes = TextField()

    class Meta:
        database = DATABASE
        # order_by = ('-timestamp',)

class MyLibrary(Model):
    # timestamp = DateTimeField(default=datetime.datetime.now)
    user_id = ForeignKeyField(model=User, backref="user")
    book_id = ForeignKeyField(model=Book, backref="book")

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Book, User, Goal, MyLibrary], safe=True)
    DATABASE.close()