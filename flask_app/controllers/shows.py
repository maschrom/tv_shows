from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.show import Show
from flask_app.models.user import User

@app.route("/shows/form")
def show_form():
    return render_template("show_form.html")

@app.route("/shows/<int:id>")
def show(id):
    data = {
        "id" : id
    }
    show = Show.get_by_id(data)
    user = User.get_by_id(data)
    return render_template("show.html", show = show, user = user)

@app.route("/shows/save", methods=["post"])
def save_show():
    if not Show.validate_show(request.form):
        return redirect("/shows/form")
    data = {
        "name" : request.form["name"],
        "network" : request.form["network"],
        "date_made" : request.form["date_made"],
        "description" : request.form["description"],
        "user_id" : request.form["user_id"]
    }
    Show.save(data)
    return redirect("/dashboard")

@app.route("/shows/<int:id>/edit")
def edit_show(id):
    data = {
        "id" : id
    }
    show = Show.get_by_id(data)
    return render_template("edit_show.html", show = show)

@app.route("/shows/<int:id>/update", methods=["post"])
def update_show(id):
    if not Show.validate_show(request.form):
        return redirect("/dashboard")
    data = {
        "id" : id,
        "name" : request.form["name"],
        "network" : request.form["network"],
        "date_made" : request.form["date_made"],
        "description" : request.form["description"],
        "user_id" : request.form["user_id"]
    }
    Show.update(data)
    return redirect("/dashboard")

@app.route("/shows/<int:id>/delete")
def delete_show(id):
    data = {
        "id" : id
    }
    Show.delete(data)
    return redirect("/dashboard")
