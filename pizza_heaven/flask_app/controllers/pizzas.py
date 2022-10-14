from django.shortcuts import render
from flask import Flask, render_template, request, session, redirect, flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.pizza import Pizza


@app.route("/dashboard")
def dashboard():
    
    if "user_id" not in session:
        flash("you must be logged in to view this page", "login")
        return redirect("/home")
    data = {
        "id": session['user_id']
    }
    current_user = User.get_one(data)
    pizzas_made = Pizza.get_pizza_and_seller()

    return render_template("dashboard.html", pizzas=pizzas_made, current_user=current_user)


@app.route("/make_pizza")
def make():
    return render_template("make.html")

@app.route("/save_pizza", methods=['post'])
def save_pizza():
    if "user_id" not in session:
        flash("you must be logged in to view this page", "login")
        return redirect("/home")

    data = {
        "pizza_name": request.form['pizza_name'],
        "description": request.form['description'],
        "toppings": request.form['toppings'],
        "user_id": request.form['user_id']
    }

    Pizza.save(data)
    return redirect("/dashboard")


@app.route("/heavenly/<int:pizza_id>/<int:heavenly_counter>")
def heavenly(pizza_id, heavenly_counter):
    if "user_id" not in session:
        flash("you must be logged in to view this page", "login")
        return redirect("/home")
    heavenly_counter += 1

    data = {
        "id": pizza_id,
        "heavenly": heavenly_counter
    }
    Pizza.inc_heaven(data)
    return redirect("/dashboard")



@app.route("/heretic/<int:pizza_id>/<int:heresy_counter>")
def heretic(pizza_id, heresy_counter):
    if "user_id" not in session:
        flash("you must be logged in to view this page", "login")
        return redirect("/home")
    
    heresy_counter += 1

    data = {
        "id": pizza_id,
        "heresy": heresy_counter
    }
    Pizza.inc_heresy(data)
    return redirect("/dashboard")


@app.route("/delete/<int:pizza_id>")
def delete_pizza(pizza_id):
    if "user_id" not in session:
        flash("you must be logged in to view this page", "login")
        return redirect("/home")
    data = {
        "id": pizza_id
    }
    Pizza.delete(data)
    return redirect("/dashboard")


@app.route("/view/<int:pizza_id>")
def view_pizza(pizza_id):
    if "user_id" not in session:
        flash("you must be logged in to view this page", "login")
        return redirect("/home")
    data = {
        "id": pizza_id
    }
    users_check = Pizza.get_pizza_and_seller()
    user_pizza = Pizza.get_pizza(data)

    return render_template("view.html", pizza=user_pizza, users=users_check)

@app.route("/edit/<int:pizza_id>")
def edit(pizza_id):
    if "user_id" not in session:
        flash("you must be logged in to view this page", "login")
        return redirect("/home")
    data = {
        "id": pizza_id
    }
    pizza = Pizza.get_by_id(data)

    return render_template("edit.html", pizza=pizza)

@app.route("/update/<int:pizza_id>", methods=['post'])
def update(pizza_id):
    if "user_id" not in session:
        flash("you must be logged in to view this page", "login")
        return redirect("/home")
    data = {
        "id": pizza_id,
        "pizza_name": request.form['pizza_name'],
        "description": request.form['description'],
        "toppings": request.form['toppings']
    }
    Pizza.update(data)
    return redirect("/dashboard")


@app.route("/view_user/<int:user_id>")
def view_user_profile(user_id):
    if "user_id" not in session:
        flash("you must be logged in to view this page", "login")
        return redirect("/home")
    data = {
        "id": user_id
    }
    users = User.get_one(data)
    pizzas = Pizza.get_pizzas_for_one_user(data)
    return render_template("view_user.html", pizzas=pizzas, user=users)