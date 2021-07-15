from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required
from werkzeug.security import generate_password_hash

from models import User, Pais,PaisUser
from flask_app import db
from perms import roles

cli = Blueprint('cliente', __name__)


# Adicionar Produto
@cli.route('/addcliente', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def criar():
    if request.method == 'POST':
        # Ir buscar dados ao html

        nome = request.form.get('nome')
        email = request.form.get('email')
        tele = request.form.get('tel')
        pais = request.form.getlist('pais')
        leads = request.form.get('leads')
        password = request.form.get('password')
        # Adicionar na bd
        user = User(name=nome, role="Cliente", email=email, tel=tele, leads=leads,
                    password=generate_password_hash(password, "sha256"))
        db.session.add(user)
        db.session.commit()
        for data in pais:
            paisuser = PaisUser(user=user.id, pais=data)
            db.session.add(paisuser)
            db.session.commit()
        flash("Cliente adicionado", category="success")
        return redirect(url_for('cliente.lista'))

    return render_template("cliente/criar.html", pais=Pais.query.all())


# Listar produto
@cli.route('/cliente', methods=['GET', 'POST'])
@login_required
@roles('Admin')
def lista():
    return render_template("cliente/lista.html", cliente=User.query.filter_by(role='Cliente'),pais=Pais.query.all(),paisuser=PaisUser.query.all())


# Apagar Produto
@cli.route('/cliente/<int:id>/delete', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def apagar(id):
    cliente = User.query.get_or_404(id)
    if cliente and cliente.role == "Cliente":
        db.session.delete(cliente)
        db.session.commit()
    else:
        flash("Cliente não existe", "error")
    return redirect(url_for('cliente.lista'))


@cli.route('/cliente/<int:id>/update', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def update(id):
    cliente = User.query.get_or_404(id)
    if request.method == 'POST':
        if cliente and cliente.role == "Cliente":
            cliente.name = request.form.get('nome')
            cliente.email = request.form.get('email')
            cliente.tel = request.form.get('tele')
            cliente.pais = request.form.get('pais')
            cliente.leads = request.form.get('leads')
            cliente.password = request.form.get('senha')

            db.session.commit()
            return redirect(url_for('cliente.lista'))
        flash("Cliente não existe", "error")

    return render_template('cliente/editar.html', data=cliente)
