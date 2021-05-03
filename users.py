from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import User
from flask_app import db
from perms import roles

user = Blueprint('users', __name__)


# Mostrar lista de utilizadores
@user.route('/users', methods=['GET', 'POST'])
@login_required
@roles('Admin')
def users():
    return render_template("users.html", user=current_user, userss=User.query.all())


# Apagar Utilizador
@user.route('/user/<int:id>/delete', methods=['GET', 'POST'])
@roles("Admin")
def delete_user(id):
    user = User.query.get_or_404(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    else:
        flash("Usuario não existe", "error")
    return redirect(url_for('users.users'))


@user.route('/user/<int:id>/update', methods=['GET', 'POST'])
@login_required
@roles("Admin")
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
            return redirect(url_for('users.users'))
        return f"Employee with id = {id} Does nit exist"

    return render_template('usere.html', userr=user)
