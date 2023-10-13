from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_session import Session
from flask_login import LoginManager, login_manager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

app = Flask(__name__, template_folder="views")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Session(app)
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from application.models import *
from application import routes