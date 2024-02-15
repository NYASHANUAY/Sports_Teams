from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re


DATABASE = "sports_db"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data["last_name"]
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "insert into users (first_name, last_name,  email , password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"

        # comes back as the new row id
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def get_by_id(cls, user_id):
        query = "select * from users where id = %(user_id)s;"
        data = {
            "user_id": user_id
        }
        result = connectToMySQL(DATABASE).query_db(query, data)
        user_info = cls(result[0])
        return user_info

    @classmethod
    def get_by_email(cls, data):
        query = "select * from users where email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        user_info = cls(result[0])
        return user_info

    @staticmethod
    def validate_user(data):
        is_valid = True  # we assume this is true
        if len(data['first_name']) < 2:
            flash("Name must be at least 3 characters.", "reg")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Name must be at least 3 characters.", "reg")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "reg")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.", "reg")
            is_valid = False
        return is_valid
