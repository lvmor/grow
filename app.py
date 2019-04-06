from flask import Flask, g
from flask import render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user 
from flask_bcrypt import check_password_hash
import json


import models
import forms
from forms import BookForm, GoalForm

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'supersecret'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route("/register", methods=("GET", "POST"))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You are now registered!", "success")
        models.User.create_user(
            name = "N/A",
            username = form.username.data,
            email = form.email.data,
            password = form.password.data,            
            avatar = "N/A",
            genre = "N/A")

        return redirect(url_for("index"))
    return render_template("register.html", form=form)

@app.route("/login", methods=("GET", "POST"))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("your emails or password does not match", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in", "success")
                return redirect(url_for("index"))
            else:
                flash("your email or password does not match" "error")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out", "success")
    return redirect(url_for("index"))

@app.route("/", methods=["GET", "POST"])
def index():
    form = BookForm()
    if form.validate_on_submit():
        models.Book.create(
        image = form.image.data.strip(),
        title = form.title.data.strip(),
        author = form.author.data.strip(),
        ISBN_10 = form.ISBN_10.data.strip(),
        current_page = form.current_page.data,
        total_pages = form.total_pages.data)
        flash("Added new book, titled: {}".format(form.title.data))
        return redirect("/setgoal")
        # return redirect('/books/{}'.format(book_id))
            
    return render_template("add_book.html", title = "Add Form", form = form )
    # with open("books.json") as json_data:
    #     books_data = json.load(json_data)
    #     return render_template("books.html", books_template = books_data)

@app.route("/about")
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/books")
@app.route("/books/")
@app.route("/books/<book_id>", methods=["GET", "POST"])
def books(book_id = None):
    if book_id == None:
        books_data = models.Book.select().limit(24)
        return render_template("books.html", books_template = books_data)
    else:
        book_ID = int(book_id)
        book = models.Book.get(models.Book.id == book_ID )
        return render_template("book.html", book = book)

    # with open ('books.json') as json_data:
    #     books_data = json.load(json_data)
    #     if book_id == None:
    #         return render_template("books.html", books_template = books_data)
    #     else:
    #         book_ID = int(book_id)
    #         return render_template("book.html", book = books_data[book_ID])

@app.route("/mybooks")
@app.route("/mybooks/")
def mybooks():
    books = models.Book.select().limit()
    return render_template("mybooks.html")

@app.route("/setgoal", methods=["GET", "POST"])
@app.route("/setgoal/", methods=["GET", "POST"])
def setgoal():
    form = GoalForm()
    if form.validate_on_submit():
        models.Goal.create(
            # user_id = current_user.id,
            # book_id = book_id,
            start_date = form.start_date.data.strip(),
            end_date = form.end_date.data.strip(),
            book_progress = form.book_progress.data.strip(),
            status = form.status.data.strip(),
            total_books_read = form.total_books_read.data,
            notes = form.notes.data.strip()
        )
        return redirect ("/mybooks")
    return render_template("set_goal.html", title="New Goal", form=form)

@app.route("/mygoals")
@app.route("/mygoals/")
@app.route("/mygoals/<goal_id>")
def mygoals(goal_id = None):
    with open("goals.json") as json_data:
        goals_data = json.load(json_data)
        if goal_id == None:
            return render_template("mygoals.html", goals_template = goals_data)
        else:
            goal_ID = int(goal_id)
            return render_template("mygoal.html", goal = goals_data[goal_ID])

@app.route("/stats")
@app.route("/stats/")
def stats():
    return render_template("stats.html")

@app.route("/achievements")
@app.route("/achievements/")
def achievements():
    return render_template("achievements.html")

if __name__ == '__main__':
    models.initialize()
    # try:
    #     models.User.create_user(
    #         name = "Mr. User",
    #         username = "mr.username",
    #         email = "user@io.com",
    #         password = "dog",
    #         avatar = "user.png",
    #         genre = "Self-development"
    #         )
    # except ValueError:
    #     pass

    app.run(debug=DEBUG, port=PORT)
