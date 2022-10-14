from unittest import result
from flask_app.config.connector import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user



class Pizza:
    DB = "pizza_heaven"
    def __init__(self,data):
        self.id = data['id']
        self.pizza_name = data['pizza_name']
        self.description = data['description']
        self.toppings = data['toppings']
        self.heavenly = data['heavenly']
        self.heresy = data['heresy']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO pizzas (pizza_name,description,toppings,user_id) VALUES (%(pizza_name)s,%(description)s,%(toppings)s,%(user_id)s);"

        result = connectToMySQL(cls.DB).query_db(query,data)

        return result

    
    @classmethod
    def inc_heaven(cls,data):
        query = "UPDATE pizzas SET heavenly = %(heavenly)s WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def inc_heresy(cls,data):
        query = "UPDATE pizzas SET heresy = %(heresy)s WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM pizzas WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_pizza(cls,data):
        query = "SELECT * FROM pizzas WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM pizzas WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if result:
            pizza = cls(result[0])
            return pizza
        return False

    @classmethod
    def update(cls,data):
        query = "UPDATE pizzas SET pizza_name = %(pizza_name)s, description = %(description)s, toppings = %(toppings)s WHERE id = %(id)s"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_pizzas_for_one_user(cls,data):
        query = "SELECT * FROM pizzas LEFT JOIN users ON pizzas.user_id = users.id WHERE users.id = %(id)s;"

        result = connectToMySQL(cls.DB).query_db(query,data)
        all_pizzas = []
        for row in result:
            one_pizza = cls(row)

            one_pizza_user_info = {
                'id': row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }

            pizza_jerk = user.User(one_pizza_user_info)
            one_pizza.creator = pizza_jerk
            all_pizzas.append(one_pizza)
        return all_pizzas

    @classmethod
    def get_pizza_and_seller(cls):
        query = "SELECT * FROM pizzas LEFT JOIN users ON pizzas.user_id = users.id;"

        result = connectToMySQL(cls.DB).query_db(query)
        all_pizzas = []
        for row in result:
            one_pizza = cls(row)

            one_pizza_user_info = {
                'id': row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }

            pizza_jerk = user.User(one_pizza_user_info)
            one_pizza.creator = pizza_jerk
            all_pizzas.append(one_pizza)
        
        return all_pizzas