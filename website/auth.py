from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password! Try again', category='fail')
        else:
            flash('User with this username doesnt exits!', category='fail')

    return render_template("login.html", user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('User already exists!.', category='fail')
        elif len(username) < 4:
            flash('Username must be greater than 4 characters.', category='fail')
        elif password1 != password2:
            flash('Passwords do not match!', category='fail')     
        elif len(password1) < 6:
            flash('Password must be greater than 6 characters.', category='fail')
        else:
            new_user = User(username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account has been created! You can now log in!', category='success')
            return redirect(url_for('auth.login'))


    return render_template("sign-up.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    
@auth.route('/delete/<int:id>', methods=['DELETE','POST'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return { "message": "User deleted." }
    else:
        return { "message": "User not found." }



