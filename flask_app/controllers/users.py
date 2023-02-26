from flask_app.models.user import User
from flask_app.models.show import Show
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template, request, redirect, session, flash

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if not "user_id" in session:
        redirect("/")
    id = session["user_id"]
    user_data = {
        "id" : id
    }
    user = User.get_by_id(user_data)
    shows = Show.get_all()
    return render_template("dashboard.html", user = user, shows = shows)

@app.route("/users/register", methods=["post"])
def register():
    if not User.user_validation(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    form_data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash
    }
    user_id = User.save(form_data)
    session["user_id"] = user_id
    return redirect("/dashboard")

@app.route("/users/login", methods=["post"])
def login():
    if not User.validate_login(request.form):
        return redirect("/")
    form_data = {
        "email" : request.form["email"]
    }
    user = User.get_by_email(form_data)
    print(user.password)
    if user:
        if not bcrypt.check_password_hash(user.password, request.form["password"]):
            flash("Email/Password combination is incorrect")
            return redirect("/")
        session["user_id"] = user.id
        return redirect("/dashboard")
    flash("Email was not found")
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")