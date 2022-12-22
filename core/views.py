from . import app, get_db
from core.util import get_session_key
from flask import render_template, redirect, session

import logging


@app.route('/')
def landing_page():
    db = get_db()
    email = None
    if 'jwt' in session:
        email = get_session_key()
        if db.hgetall(email):
            pass
        else:
            redirect('/logout')
    
    return render_template('home.html', Name="Home", EMAIL=email)


@app.route("/login", methods=["GET"])
def login_test():
    db = get_db()
    email = None

    if 'jwt' in session:
        email = get_session_key()
        if db.hgetall(email):
            return redirect('/dashboard')
        else:
            return redirect('/logout')
    return render_template('login.html', Name="Login", EMAIL=email)

    
@app.route("/register", methods=["GET"])
def register_view():
    db = get_db()
    email = None

    if 'jwt' in session:
        email = get_session_key()
        if db.hgetall(email):
            return redirect('/dashboard')
        else:
            return redirect('/logout')
    return render_template('register.html', Name="Register", EMAIL=email)


@app.route("/logout", methods=["GET"])
def logout():
    if ('jwt' in session):
        del session['jwt'] 
    return redirect('/login')

