
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password=request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Login in successful',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, Try again.', category='error')
        else:
            flash("No user registered with given Email",category='error')
    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup',methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user=User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category='error')
        elif len(email)<7:
            flash('Email must be greater than 6 characters.',category='error')
        elif len(firstName)<3:
            flash('First name must be greater than 2 characters.',category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.',category='error')
        elif len(password1)<8 or len(password2) <8:
            flash('Password must be atleast 7 characters.',category='error')
        else:
            new_user = User(email=email,first_name = firstName,password=generate_password_hash(password1,method='pbkdf2:sha256'))

            db.session.add(new_user)
            db.session.commit()
            login_user(user,remember=True)
            flash("Accout created successfully.", category='success')

            return redirect(url_for('views.home'))
    return render_template("signup.html",user=current_user)
