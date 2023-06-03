
import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tepyicha.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == "POST":
        email = request.form.get("email")
        password =request.form.get("password")

        if email == "" or password =="" :
            return render_template("login.html", msg1="Veuillez ramplir tous les champs du formulaire")

        a = db.execute("SELECT email FROM clients WHERE email = ?", email)
        print(len(a))
        if (len(a) == 0) == True:
            return render_template("login.html", msg1="Invalid password Or Email ", msg=" Are you Already Registred !")

        password_saved  = db.execute("SELECT password FROM clients WHERE email = ?", email)
        print(password_saved)
        print(password_saved[0]["password"])
        if password_saved[0]["password"] == password:
            user = db.execute("SELECT id FROM clients WHERE email=?",email)

            session["user_id"] = user[0]["id"]
            flash("Welcome Back")
            return render_template("index.html")
        else:
            return render_template("login.html", msg1="invalid password")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    flash("Good Bye")
    # Redirect user to login form
    return redirect("/")

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # si inputs est vide
        username = request.form.get("username")
        email = request.form.get("email")
        password =request.form.get("password")

        if username == "" or email == "" or password =="" :
            return render_template("register.html", msg="Veuillez ramplir tous les champs du formulaire")
        if (len(password) < 6) == True:

            return render_template("register.html", msg="le password doit au moin avoir 6 charactere")

        #si l'email est deJa enregisres
        a = db.execute("SELECT email FROM clients WHERE email =?",email)
        print(a)

        if (len(a) == 1) == True:
            return render_template("register.html", msg="Email Déja inscrit", msg2="login !")

        db.execute("INSERT INTO clients (username, email, password) VALUES(?, ?, ?)",username, email, password)
        b= db.execute("SELECT username FROM clients WHERE email=?",email)
        print(b)
        l=b[0]["username"]
        flash("Welcome")
        return render_template("/register.html", msg1=l, msg2=" Succesfull Registration  mrs/mdms :   ")

    else:
        return render_template("/register.html")
