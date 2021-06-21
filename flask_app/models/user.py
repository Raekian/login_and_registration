# from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# from flask_app.models import *any relationship model you need to pull

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    def __init__(self, data):
        self.id = data['id'],
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password =data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 3:
            flash("first name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("email must be at least 6 characters must be a valid email.")
            is_valid = False
        if len(user['password']) < 3:
            flash("password must be at least 3 characters.")
            is_valid = False
        return is_valid

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        results = connectToMySQL('login_and_registration').query_db(query, data)
        print(results)
        return results

    @classmethod
    def get_users(cls, data):
        query = "SELECT * FROM users;"
        results = connectToMySQL('login_and_registration').query_db(query, data)
        return results

    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM USERS WHERE users.id = %(id)s;"
        results = connectToMySQL('login_and_registration').query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query ="SELECT * FROM USERS WHERE users.email = %(email)s;"
        results = connectToMySQL('login_and_registration').query_db(query, data)
        if len(results) <1:
            return False
        return cls(results[0])