from flask_app import app
from flask import flash
import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

db="log_and_reg"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")



class User:
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @staticmethod
    def validate(data):
        is_valid=True
        if len(data['first_name'])<2:
            flash("First name must be at least 2 characters.")
            is_valid=False
        if len(data['last_name']) <2:
            flash("Last name must be at least 2 characters.")
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash('Email is not valid. Please try again. ')
            is_valid=False
        if User.get_by_email({'email':data['email']}):
            flash('Email is already in use.')
            is_valid=False
        if not PASS_REGEX.match(data['password']):
            flash("Password must contain at least 8 characters, 1 Uppercase, 1 Lowercase, 1 Number!","register")
            is_valid=False
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match. Please try again.')
            is_valid=False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query='SELECT * FROM users WHERE email = %(email)s'
        data=connectToMySQL(db).query_db(query,data)
        if data== ():
            return False
        else:
            return cls(data[0])


    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL(db).query_db(query,data)
