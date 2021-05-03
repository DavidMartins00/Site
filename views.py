from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import update

from models import User
import json
from flask_app import db
from perms import roles

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)






