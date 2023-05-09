import os
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import requests
from cs50 import SQL
from functools import wraps

app = Flask(__name__)

API_KEY = "eb45f9e1e434980920ee4c76f0295865"
URL = "https://api.themoviedb.org/3/search/movie?api_key=" + API_KEY + "&query="
db = SQL("sqlite:///movie-search.db")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
@app.route("/index")
def index():
    print(session)
    return render_template("index.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        search = request.form["search"]
        search = URL + search
    response = requests.get(url=search)
    response.raise_for_status
    dict = response.json()
    for i in dict["results"]:
        if not i["poster_path"]:
            i[
                "poster_path"
            ] = "https://previews.123rf.com/images/alekseyvanin/alekseyvanin1812/alekseyvanin181202067/114068021-search-not-found-vector-icon-filled-flat-sign-for-mobile-concept-and-web-design-magnifier-with.jpg"
        else:
            i["poster_path"] = "https://image.tmdb.org/t/p/w300" + i["poster_path"]
    return render_template("index.html", list=dict["results"])


@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favorites():
    if request.method == "POST":
        movie_id = int(request.form["movie_id"])
        image = str(request.form["image"])
        title = str(request.form["title"])
        date = str(request.form["date"])
        vote = str(request.form["vote"])
        user_id = int(session["user_id"])
        db.execute(
            "INSERT INTO favorites (user_id, movie_id, image, title, date, vote) VALUES (?);",
            (user_id, movie_id, image, title, date, vote),
        )
    user_id = session["user_id"]
    user_list = db.execute(f"SELECT * FROM favorites WHERE user_id = {user_id}")
    return render_template("favorites.html", list=user_list)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        # Ensure password was submitted
        password = request.form.get("password")
        rows = db.execute("SELECT * FROM user WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not (rows[0]["password"] == password):
            return redirect("/login")
        print(username)
        print(password)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        print(session)
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        users = db.execute("SELECT username FROM user")
        print(users)
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password == confirmation:
            db.execute(
                "INSERT INTO user (username, password) VALUES(?, ?)",
                username,
                password,
            )
            return redirect("/")
        else:
            return redirect("/register")
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
