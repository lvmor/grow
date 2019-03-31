from flask_wtf import FlaskForm as Form
from wtforms import TextField, IntegerField, SubmitField

from models import Book

class BookForm(Form):
    title = TextField("Title: ")
    image = TextField("Image: ")
    author = TextField("Author: ")
    ISBN_10 = TextField("ISBN: ")
    current_page = IntegerField("Current page: ")
    total_pages = IntegerField("Total pages")
    submit = SubmitField("Add Book")