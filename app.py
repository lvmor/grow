from flask import Flask, g
from flask import render_template, flash, redirect, url_for, request
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
        flash("You are now registered!", "alert alert-success")
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
            flash("Your email/password does not match", "alert alert-danger")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You are now logged in", "alert alert-success")
                return redirect(url_for("index"))
            else:
                flash("Your email/password does not match", "alert alert-danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out!", "alert alert-warning")
    return redirect(url_for("index"))

@app.route("/delete/<goal_id>", methods=["GET", "POST"])
def delete(goal_id):
    flash("You have deleted a book goal", "alert alert-warning")
    models.Goal.delete_by_id(goal_id)
    return redirect("/mygoals")


@app.route("/", methods=["GET", "POST"])
def index():
    form = BookForm()
    if form.validate_on_submit():
        models.Book.create(
        image = form.image.data.strip(),
        title = form.title.data.strip(),
        author = form.author.data.strip(),
        ISBN_13 = form.ISBN_13.data.strip(),
        ISBN_10 = form.ISBN_10.data.strip(),
        date_published = form.date_published.data.strip(),
        description = form.description.data.strip(),
        total_pages = form.total_pages.data)
        flash("Added new book, titled: {}".format(form.title.data), "alert alert-success")
        return redirect("/setgoal")
        # return redirect('/books/{}'.format(book_id))
            
    return render_template("add_book.html", title = "Add Form", form = form)

    # form = BookForm()
    # bookid = request.form.get("bookid", "")
    # command = request.form.get("submit", "")

    # if command == "Delete":
    #     models.Book.delete_by_id(bookid)
    #     return redirect("/mybooks")
    # elif command == "Edit":
    #     bookid = int(bookid)
    #     book = models.Book.get(models.Book.id == bookid)
    #     form.id.data = book.id
    #     form.title.data = goal.title
    #     form.image.data = goal.image
    #     form.author.data = goal.author
    #     form.ISBN_10.data = goal.ISBN_10
    #     form.total_pages.data = goal.total_pages
    #     return render_template("/mybooks.html", book=book, goal=goal, form=form)

    # if form.validate_on_submit():
    #     if form.id. data == "":
    #         models.Book.create(
    #             # user_id = current_user.id,
    #             title = form.title.data.strip(),
    #             image = form.image.data.strip(),
    #             author = form.author.data.strip(),
    #             ISBN_10 = form.ISBN_10.data.strip(),
    #             total_pages = form.total_pages.data)
            
    #         return redirect ("/mybooks")
    #     else:
    #         book = models.Book.get(models.Book.id == form.id.data)
    #         book.title = form.title.data.strip()
    #         book.image = form.image.data.strip()
    #         book.author = form.author.data.strip()
    #         book.ISBN_10 = form.ISBN_10.data.strip()
    #         book.total_pages = form.total_pages.data
    #         book.save()
    #         flash("Added new book, titled: {}".format(form.title.data), "alert alert-success")
    #         return redirect("/mybooks")

    # return render_template("/mybooks.html", book=book, goal=goal, form=form)

@app.route("/about")
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/books")
@app.route("/books/")
@app.route("/books/<book_id>", methods=["GET", "POST"])
def books(book_id = None):
    if book_id == None:
        search = request.args.get("search")
        if search == "":
            books_data = models.Book.select().limit(24)
        else:
            books_data = models.Book.select().where(models.Book.title.contains(search)).limit(24)

            # amazon = AmazonAPI("jqwlxzk96k", "QTBsZPRuzC963Om8oLirb5fAI5sY8jbJ1ZMQvOg1", "bookgoals-20")
        return render_template("books.html", books_template = books_data)
    else:
        book_ID = int(book_id)
        book = models.Book.get(models.Book.id == book_ID)
        return render_template("book.html", book = book)

@app.route("/mybooks")
@app.route("/mybooks/")
@login_required
def mybooks():
    books = models.Book.select().limit()
    return render_template("mybooks.html")

@app.route("/setgoal", methods=["GET", "POST"])
@app.route("/setgoal/", methods=["GET", "POST"])
@app.route("/setgoal/<book_id>", methods=["GET", "POST"])
@login_required
def setgoal(book_id = None):
    form = GoalForm()
    if form.validate_on_submit():
        found = models.Goal.select().where(models.Goal.user_id == current_user.id and models.Goal.book_id == book_id)
        print(found.count())
        if found.count()  == 0:
            models.Goal.create(
            user_id = current_user.id,
            book_id = book_id,
            start_date = form.start_date.data,
            end_date = form.end_date.data,
            book_progress = 0,
            status = "In-progress",
            notes = form.notes.data.strip())
            flash("Added a new book goal!", "alert alert-success")
        else:
            flash("You have already set a goal for this book", "alert alert-warning")
        return redirect ("/mygoals")

    return render_template("set_goal.html", title="New Goal", form=form)



@app.route("/mygoals")
@app.route("/mygoals/")
@app.route("/mygoals/<goal_id>", methods=["GET", "POST"])
@login_required
def mygoals(goal_id = None):
    if goal_id == None:
        goals_data = models.Goal.select().limit(10)
        return render_template("mygoals.html", goals_template = goals_data)
    # goalid = request.form.get("goalid", "")
    # command = request.form.get("submit", "")

    # if command == "Delete":
    #     models.Goal.delete_by_id(goalid)
    #     return redirect("/mygoals")
    else:
        goal_ID = int(goal_id)


        goal = models.Goal.get(models.Goal.id == goal_ID)
        if request.method == "POST":
            pages = int(request.form["pages"])
            if pages >= 0 and pages <= goal.book_id.total_pages:
                goal.book_progress = pages
                goal.save()
                flash("Your goal has been updated!", "alert alert-success")
            else:
                flash("Cannot update. Incorrect value for pages.", "alert alert-danger")
        progress = int((goal.book_progress / goal.book_id.total_pages) * 100)
        return render_template("mygoal.html", goal = goal, progress = progress)

    # form = GoalForm()
    # goalid = request.form.get("goalid", "")
    # command = request.form.get("submit", "")

    # if command == "Delete":
    #     models.Goal.delete_by_id(goalid)
    #     return redirect("/mygoals")
    # elif command == "Edit":
    #     goal_ID = int(goal_id)
    #     goal = models.Goal.get(models.Goal.id == goal_ID)
    #     progress = int((goal.book_progress / goal.book_id.total_pages) * 100)
    #     form.id.data = goal.id
    #     form.start_date.data = goal.start_date
    #     form.end_date.data = goal.end_date
    #     form.book_progress.data = goal.book_progress
    #     form.status.data = goal.status
    #     form.total_books_read.data = goal.total_books_read
    #     form.notes.data = goal.notes
    #     return render_template("mygoal.html", goal = goal, progress = progress)

    # if form.validate_on_submit():
    #     if form.id. data == "":
    #         models.Goal.create(
    #             # user_id = current_user.id,
    #             # book_id = book_id,
    #             # book = book,
    #             start_date = form.start_date.data.strip(),
    #             end_date = form.end_date.data.strip(),
    #             book_progress = form.book_progress.data.strip(),
    #             status = form.status.data.strip(),
    #             total_books_read = form.total_books_read.data,
    #             notes = form.notes.data.strip())
            
    #         return redirect ("/mybooks")
    #     else:
    #         goal = models.Goal.get(models.Goal.id == form.id.data)
    #         goal.start_date = form.start_date.data.strip()
    #         goal.end_date = form.end_date.data.strip()
    #         goal.book_progress = form.book_progress.data.strip()
    #         goal.status = form.status.data.strip()
    #         goal.total_books_read = form.total_books_read.data
    #         goal.notes = form.notes.data.strip()
    #         goal.save()
    #         flash("Added a new book goal!", "alert alert-success")
    #         return redirect("/mygoals/{}".format(goal_id))

    # return render_template("mygoal.html", goal = goal, progress = progress)

@app.route("/stats")
@app.route("/stats/")
@login_required
def stats():
    return render_template("stats.html")

@app.route("/achievements")
@app.route("/achievements/")
@login_required
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
