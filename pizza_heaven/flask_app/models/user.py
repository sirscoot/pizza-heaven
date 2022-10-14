from unittest import result
from flask_app.config.connector import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import pizza
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = "pizza_heaven"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pizzas = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW());"

        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    


    
    @staticmethod
    def validator(user):
        is_valid = True

        query = "SELECT * FROM users WHERE email = %(email)s;"

        result = connectToMySQL(User.DB).query_db(query,user)

        if len(result) >= 1:
            flash("Another user is registered under this email", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("first name can't be less than 3 characters", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("last name can't be less than 3 characters", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("password must contain more than 8 characters", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("passwords do not match", "register")
            is_valid = False
        return is_valid