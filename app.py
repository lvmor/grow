from flask import Flask, g, jsonify
from flask import render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
import json
import os
from playhouse.shortcuts import model_to_dict, dict_to_model

# import numpy as np
# import plotly.graph_objs as go
# import plotly.offline as ply
# import dash
# from dash.dependencies import Output, Event
# import dash_core_components as doc
# import dash_html_components as html
# import plotly
# import random
# import plotly.graph_objs as go
# from collections import deque


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
        results = models.Book.select().where(models.Book.ISBN_13 == form.ISBN_13.data.strip() or models.Book.ISBN_10 == form.ISBN_10.data.strip()).limit(1)
        if len(results) > 0:
            book = results[0]            
        else:
            book = None
        if book == None:
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
            book = models.Book.get(models.Book.ISBN_13 == form.ISBN_13.data.strip() or models.Book.ISBN_10 == form.ISBN_10.data.strip())
        return redirect("/setgoal/{}".format(book.id))
            
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

# TODOS:
# [] filter books_data to only show books that HAVE NOT yet been added
# [] comment out the mybooks route, test the app to check for breaks
# [] remove my library from navbar
# [] move "Set Goal" functionality to the My Library list
# [X] rename "Set Goal" nav item to something else
# [] rename/remove the set pages goal on the set goal page

@app.route("/books")
@app.route("/books/")
@app.route("/books/<book_id>", methods=["GET", "POST"])
def books(book_id = None):
    if book_id == None:
        books_data = models.Book.select().limit(24)
        mybooks = models.MyLibrary.select().where(models.MyLibrary.user_id == current_user.id).limit(9)

        return render_template("books.html", books_template = books_data, mybooks = mybooks)
    else:
        book_ID = int(book_id)
        book = models.Book.get(models.Book.id == book_ID)
        return render_template("book.html", book = book)

@app.route("/mybooks")
@app.route("/mybooks/")
@app.route("/mybooks/<book_id>")
@login_required
def mybooks(book_id = None):
    if book_id == None:
        mybooks = models.MyLibrary.select().where(models.MyLibrary.user_id == current_user.id).limit(9)
        return render_template("mybooks.html", mybooks = mybooks)
    else:
        print("user_id = " + str(current_user.id) + ", book_id = " + book_id)
        found = models.MyLibrary.select().where(models.MyLibrary.book_id == book_id).where(models.MyLibrary.user_id == current_user.id)

        if found.count() == 0:
            models.MyLibrary.create(book_id = book_id, user_id = current_user.id)
            flash("Book has been added to your library!", "alert alert-success")
        else:
            flash("You have already added this book!", "alert alert-info")
        return redirect("/books")
        


@app.route("/setgoal", methods=["GET", "POST"])
@app.route("/setgoal/", methods=["GET", "POST"])
@app.route("/setgoal/<book_id>", methods=["GET", "POST"])
@login_required
def setgoal(book_id = None):
    # SetGoal: Sets the reading goal for a book.
    form = GoalForm()
    if form.validate_on_submit():
        found = models.Goal.select().where(models.Goal.book_id == book_id).where(models.Goal.user_id == current_user.id)
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
        # get list of my goals - books
        goals_data = models.Goal.select().where(models.Goal.user_id == current_user.id).limit(100)
        for goal in goals_data:
            # get progress of each goal for displaying in progress bar
            goal.progress = int((goal.book_progress / goal.book_id.total_pages) * 100)
        return render_template("mygoals.html", goals_template = goals_data)
    else:
        # display details of individual goal
        goal_ID = int(goal_id)
    
        goal = models.Goal.get(models.Goal.id == goal_ID)
        if request.method == "POST":
            # updating page read count
            pages = int(request.form["pages"]) # get pages from textbox in form
            if pages >= 0 and pages <= goal.book_id.total_pages: # pages can be  0 to total pages of book
                goal.book_progress = pages
                goal.save() # save to database
                flash("Your goal has been updated!", "alert alert-success")
            else:
                flash("Cannot update. Incorrect value for pages.", "alert alert-danger")
        progress = int((goal.book_progress / goal.book_id.total_pages) * 100) # pages read / total pages of book * 100
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


# X =deque(maxlen=20)
# Y = deque(maxlen=20)
# X.append(1)
# Y.append(1)

# app = dash.Dash(__name__)
# app.layout = html.Div(
#     [doc.Graph(id="live-graph", animate =True),
#     doc.Interval (
#         id="graph-update",
#         interval=1000
#     )]
# )

# @app.callback(Output("live-graph", "figure")), events = [Event("graph-update", "inteval")]
# def graphstats():
#     X.append(X[-1]+1)
#     Y.append(X[-2]+2)

#     data = go.Scatter(
#         x=list(X),
#         y=list(Y),
#         name="Scatter",
#         mode="lines+markers"
#     )

#     return {"data: [data], "layout": go.Layout(xaxis) = dict(range=[min(X), max(X)]), (yaxis) = dict(range=[min(Y), max(Y)])}

# if __name__ == "__main__":
#     app.run_server(debug=True)

@app.route("/stats")
@app.route("/stats/")
@login_required
def stats():

    # n = 201
    # x = np.linspace(0, 2.0*np.pi, n)
    # y1 = np.sin(x)
    # y2 = np.cos(x)
    # y3 = y1 + y2
    # trace1 = go.Scatter(x = x, y1 = y1)
    # data = [trace1]

    # ply.plot(data, filename = 'simple_plot.html')
    return render_template("stats.html")

@app.route("/stats_goals")
@app.route("/stats_goals/")
@login_required
def stats_goals():
    goals = models.Goal.select().where(models.Goal.user_id == current_user.id).limit(100)
    #goals_data = model_to_dict(goals_data)
    list = []
    for goal in goals:
       g = {}
       g["goalid"] = goal.id
       g["title"] = goal.book_id.title
       g["pages"] = goal.book_id.total_pages
       g["pages_read"] = goal.book_progress
       list.append(g)
    return jsonify(list)

@app.route("/achievements")
@app.route("/achievements/")
@login_required
def achievements():
    return render_template("achievements.html")

@app.route("/achievements_goals")
@app.route("/achievements_goals/")
@login_required
def achievements_goals():
    # returns total pages read by user

    goals = models.Goal.select().where(models.Goal.user_id == current_user.id)
    #goals_data = model_to_dict(goals_data)
    progress = {}
    pages_read = 0
    pages_all = 0
    for goal in goals:       
       pages_read += goal.book_progress # total pages read from book
       pages_all += goal.book_id.total_pages # total pages of book
    progress["pages_read"] = pages_read
    progress["pages_all"] = pages_all

    return jsonify(progress)

if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()

if __name__ == '__main__':
    models.initialize()

    app.run(debug=DEBUG, port=PORT)
