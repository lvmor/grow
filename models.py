import datetime
from peewee import *

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

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

class Goal(Model):
    user_id = ForeignKeyField(model=User, backref="users")
    book_id = ForeignKeyField(model=Book, backref="books")
    start_date = TextField()
    end_date = TextField()
    book_progress = TextField()
    status = TextField()
    total_books_read = IntegerField()
    notes = TextField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Book, User, Goal], safe=True)
    DATABASE.close()