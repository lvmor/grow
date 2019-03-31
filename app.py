from flask import Flask, g
from flask import render_template, flash, redirect, url_for
import json

# import models

DEBUG = True
PORT = 8000

app = Flask(__name__)

# @app.before_request
# def before_request():
#     g.db = models.DATABASE
#     g.db.connect()

# @app.after_request
# def after_request(response):
#     g.db.close()
#     return response

@app.route("/")
def index():
    with open("books.json") as json_data:
        books_data = json.load(json_data)
        return render_template("books.html", books_template = books_data)

@app.route("/about")
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/books")
@app.route("/books/")
@app.route("/books/<book_id>")
def books(book_id = None):
    with open ('books.json') as json_data:
        books_data = json.load(json_data)
        if book_id == None:
            return render_template("books.html", books_template = books_data)
        else:
            book_ID = int(book_id)
            return render_template("book.html", book = books_data[book_ID])

@app.route("/mybooks")
@app.route("/mybooks/")
def mybooks():
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

if __name__ == '__main__':
    # models.initialize()
    app.run(debug=DEBUG, port=PORT)
