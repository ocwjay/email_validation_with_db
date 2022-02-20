from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Email:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def create_email(cls, data):
        query = "INSERT INTO emails (email, created_at, updated_at) VALUE (%(email)s, NOW(), NOW())"
        results = connectToMySQL('emails_schema').query_db(query, data)
        return results
    @classmethod
    def get_all_emails(cls):
        query = "SELECT * FROM emails"
        results = connectToMySQL('emails_schema').query_db(query)
        emails = []
        for email in results:
            emails.append(cls(email))
        return emails
    @classmethod
    def delete_email(cls, data):
        query = "DELETE FROM emails WHERE id = %(id)s"
        results = connectToMySQL('emails_schema').query_db(query, data)
        return results
    @staticmethod
    def validate_email(email):
        is_valid = True
        all_emails = Email.get_all_emails()
        if not EMAIL_REGEX.match(email):
            flash("Invalid email address!")
            is_valid = False
        for one_email in all_emails:
            if email == one_email.email:
                flash("Email is already registered!")
                is_valid = False
        return is_valid