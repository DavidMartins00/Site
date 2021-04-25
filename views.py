from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import User
import json
from app import db, app
from flask_principal import Principal, Permission, RoleNeed
from perms import roles

views = Blueprint('views', __name__)

principals = Principal(app)


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
def edit_user():
    user = json.loads(request.data)
    userId = user['userId']
    user = User.query.get(userId)
    if user:
        return render_template("usere.html", user=current_user, userr=user)
    return jsonify({})

    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        password = request.form.get('password')
        #Validações

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email ja existe",category="error")
        elif len(email) < 4:
            flash("Email requerido", category="error")
        elif len(nome) < 2:
            flash("Nome requerido", category="error")


        elif len(password) < 7:
            flash("Password precisa ser maior que 7 caracters", category="error")

        else:
            #Adicionar user na bd
            #edit_user =
            #db.session.add(edit_user)
            #db.session.commit()
            flash("Editar", category="success")
            return redirect(url_for('views.users'))

