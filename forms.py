from flask_wtf import FlaskForm as Form
from wtforms import TextField, IntegerField, SubmitField

from wtforms import StringField, PasswordField, TextAreaField, HiddenField
from wtforms.fields.html5 import DateField

from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                               Length, EqualTo)
from models import User, Book, Goal


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User with that name already exists.")

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("User with that email already exists.")

class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only.")
            ),
            name_exists
        ])
    email = StringField(
        "Email",
        validators = [
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        "Password",
        validators = [
            DataRequired(),
            Length(min = 2),
            EqualTo("password2", message = "Passwords must match")
        ])
    password2 =PasswordField(
        "Confirm Password",
        validators = [DataRequired()]
    )
class LoginForm(Form):
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])

class BookForm(Form):
    title = TextField("Title: ")
    image = TextField("Image: ")
    author = TextField("Author: ")
    ISBN_13 = TextField("ISBN-13: ")
    ISBN_10 = TextField("ISBN-10: ")
    date_published = TextField("date published: ")
    description = TextAreaField("description: ")
    total_pages = IntegerField("Total pages")
    submit = SubmitField("Set Goal")

class GoalForm(Form):
    id = HiddenField()
    start_date = DateField("Start date: ", validators = [DataRequired()])
    end_date = DateField("End date: ")
    # book_progress = IntegerField("Book Progress: ")
    # status = TextField("Status: ")
    notes = TextAreaField("Notes: ")
    submit = SubmitField("Save Goal")
