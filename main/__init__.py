from flask import Flask, render_template, request,redirect,url_for,flash,current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrants.db'
app.config['SECRET_KEY'] = "51f8e3190d048afd70bb5660"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 25
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = 'pujanpaudel9988@gmail.com'
app.config['MAIL_PASSWORD'] = '#Google123&'
mail = Mail(app)
