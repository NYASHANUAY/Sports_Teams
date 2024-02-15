from flask_app.models.team import Team
from flask_app import app
from flask import redirect, render_template, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/register', methods=['post'])
def registration():
    # SET UP VALIDATION. IF FAILED REDIRECT BACK TO FORM.
    if not User.validate_user(request.form):
        return redirect('/')
    # IF FORM IS GOOD SAVE TO DB. ADD USER ID AND NAME INTO SESSION AND REDIRECT TO WELCOME PAGE.
    hash_password = bcrypt.generate_password_hash(request.form['password'])
    print("bcrypt--------------------->", hash_password)
    new_form_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hash_password
    }
    user_id = User.save(new_form_data)
    print("user id--------------------->", user_id)
    session['user_id'] = user_id
    return redirect("/")


@app.route('/login', methods=['post'])
def login_user():
    user = User.get_by_email(request.form)
    print("user logging in ------------------------->", user)
    if not user:
        flash("Email/Password might be invalid", "login")
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Email/Password might be invalid", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect("/teams")


@app.route('/logout')
def logout():
    # CLEAR SESSION OF LOGGED IN USER
    session.clear()
    return redirect('/')
