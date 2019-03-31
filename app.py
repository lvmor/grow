from flask import Flask, g
from flask import render_template, flash, redirect, url_for
import json

import models

DEBUG = True
PORT = 8000

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

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

@app.route("/mybooks/<user_id>")
def mybooks(user_id):
    with open("users.json") as json_data:
        users_data = json.load(json_data)
        user_ID = int(user_id)
        return render_template("mybooks.html", user = users_data[user_ID])

@app.route("/goals/<goal_id>")
def goals(goal_id):
    with open("goals.json") as json_data:
        goals_data = json.load(json_data)
        goal_ID = int(goal_id)
        return render_template("mygoals.html", goal = goals_data[goal_ID])

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
