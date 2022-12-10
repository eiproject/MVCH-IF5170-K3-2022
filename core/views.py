from core.util import get_session_mail
from . import app, jwt, db
# from .models import Users
from flask import Flask, request, render_template, redirect, jsonify, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token


@app.route('/')
def landing_page():
    email = None
    if 'jwt' in session:
        email = get_session_mail()
        if db.hgetall(email):
            pass
        else:
            redirect('/logout')

    print("Home works!")
    return render_template('home.html', Name="Home", EMAIL=email)


@app.route("/login", methods=["GET"])
def login_test():
    email = None

    if 'jwt' in session:
        email = get_session_mail()
        if db.hgetall(email):
            print('OK')
            return redirect('/dashboard')
        else:
            return redirect('/logout')

    print("Login works!")
    return render_template('login.html', Name="Login", EMAIL=email)

    
@app.route("/register", methods=["GET"])
def register_view():
    email = None

    if 'jwt' in session:
        email = get_session_mail()
        if db.hgetall(email):
            print('OK')
            return redirect('/dashboard')
        else:
            return redirect('/logout')

    print("Register works!")
    return render_template('register.html', Name="Register", EMAIL=email)


@app.route("/logout", methods=["GET"])
def logout():
    if ('jwt' in session):
        del session['jwt'] 

    print("Logout works!")
    return redirect('/login')


@app.route("/dashboard", methods=["GET"])
def dashboard_view():
    email = None
    if 'jwt' in session:
        email = get_session_mail()
        if db.hgetall(email):
            return render_template('dashboard.html', Name="Dashboard", EMAIL=email)
        else:
            return redirect('/logout')

    