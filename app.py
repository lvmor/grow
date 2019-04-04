from flask import Flask, g
from flask import render_template, flash, redirect, url_for
import json

import models
from forms import BookForm

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'supersecret'

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

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
        print("redirect reached")
        flash("Added new book, titled: {}".format(form.title.data))
        return redirect("/mybooks")
            
    print("not working")
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
        return render_template("book.html", book = books_data[book_ID])

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
    app.run(debug=DEBUG, port=PORT)
