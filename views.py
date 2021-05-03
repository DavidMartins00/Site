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


#Mostrar lista de utilizadores
@views.route('/users', methods=['GET', 'POST'])
@login_required
@roles('Admin')
def users():

    return render_template("users.html", user=current_user, userss=User.query.all())

#Apagar Utilizador
@views.route('/delete-user', methods=['POST'])
@roles("Admin")
def delete_user():
    user = json.loads(request.data)
    userId = user['userId']
    user = User.query.get(userId)
    if user:
        db.session.delete(user)
        db.session.commit()
    return jsonify({})


@views.route('/edit-user', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def edit_user():
    user = json.loads(request.data)
    userId = user['userId']
    user = User.query.get(userId)
    if user:
        return render_template("usere.html", userr=user)


@views.route('/user/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        if user:
            user.email = request.form.get('email')
            user.name = request.form.get('nome')
            if not request.form.get('password') == "":
                user.password = request.form.get('password')
            user.role = request.form.get('role')

            db.session.commit()
            return redirect(url_for('views.users'))
        return f"Employee with id = {id} Does nit exist"

    return render_template('usere.html', userr=user)



