from flask import Flask, redirect, render_template, request
from flask_app.models.email import Email
from flask_app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    emails = Email.get_all_emails()
    return render_template('results.html', all_emails = emails)

@app.route('/email_submission', methods=['POST'])
def email_submission():
    if not Email.validate_email(request.form['email_address']):
        return redirect('/')
    data = {
        'email' : request.form['email_address']
    }
    Email.create_email(data)
    return redirect('/success')

@app.route('/email_delete/<int:id>')
def email_delete(id):
    data = {
        'id' : id
    }
    Email.delete_email(data)
    return redirect('/success')