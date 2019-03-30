from flask import Flask, g
from flask import render_template, flash, redirect, url_for
import json

DEBUG = True
PORT = 8000

app = Flask(__name__)

@app.route("/")
def index():
    with open("books.json") as json_data:
        books_data = json.load(json_data)
        return render_template("books.html", books_template = books_data)

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

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
