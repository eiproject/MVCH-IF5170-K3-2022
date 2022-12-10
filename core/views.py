from . import app, jwt, db
# from .models import Users
from flask import Flask, request, render_template, redirect, jsonify, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token


@app.route('/')
def landing_page():
    return render_template('home.html', Name="Home")


@app.route("/login", methods=["GET"])
def login_test():
    # if 'jwt' in session:
    #     session_email = decode_token(session['jwt'])['email']
    #     if Users.query.filter_by(
    #         email=session_email).first():
    #         return 'Logged in'
    print("Login works!")
    return render_template('login.html', Name="Login")

    
@app.route("/register", methods=["GET"])
def register_view():
    # if 'jwt' in session:
    #     session_email = decode_token(session['jwt'])['email']
    #     if Users.query.filter_by(
    #         email=session_email).first():
    #         return 'Logged in'
    print("Register works!")
    return render_template('register.html', Name="Register")


@app.route("/logout", methods=["GET"])
def logout():
    if ('email' in session):
        del session['email'] 
    if ('key' in session):
        del session['key']
    print("Logout works!")
    redirect('/login')