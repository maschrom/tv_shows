from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, redirect, request, session
from flask_app import app
from flask_bcrypt import Bcrypt
import pprint
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$')
bcrypt = Bcrypt(app)

class User:
    db = "tv_schema"
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.shows = []

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @staticmethod
    def user_validation(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("Your First Name is not long enough!")
            is_valid = False

        if len(user['last_name']) < 2:
            flash("Your Last Name is not long enough!")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Your email invalid!")
            is_valid = False

        if not PASSWORD_REGEX.match(user['password']) or len(user['password']) < 8:
            flash("Your password is invalid!, must have 1 uppercase, 1 lowercase, 1 digit, 1 special character")
            is_valid = False

        if not user['password'] == user['cpass']:
            flash("password and confirm password do not match!")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        user = User.get_by_email(user)
        if not user:
            flash("Email is not associated with an account")
            is_valid = False
        return is_valid
