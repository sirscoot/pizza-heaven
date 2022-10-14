import re
from flask import Flask, render_template, request, session, redirect, flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return redirect("/home")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register")
def register():
    return render_template("register.html")

# handlers
@app.route("/register_handler", methods=['post'])
def reg_handler():
    if not User.validator(request.form):
        return redirect("/home")

    new_user = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(new_user)
    session['user_id'] = id

    print(session)
    return redirect("/dashboard")

@app.route("/login_handler", methods=['post'])
def log_handler():
    data = {
        "email": request.form['email']
    }
    user = User.get_by_email(data)
    if not user:
        flash("Invalid email/password", "login")
        return redirect("/home")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid password", "login")
        return redirect("/home")
    session['user_id'] = user.id
    print(session["user_id"])
    return redirect("/dashboard")

@app.route("/logout")
def logout_handler():
    session.clear()
    print(session)
    return redirect("/home")