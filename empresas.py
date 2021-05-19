from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required
from models import Empresa
from flask_app import db
from perms import roles

empresa = Blueprint('empresa', __name__)


# Adicionar Produto
@empresa.route('/addempresa', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def criar():
    if request.method == 'POST':
        # Ir buscar dados ao html
        nome = request.form.get('nome')
        tipo = request.form.get('tipo')

        # Adicionar na bd
        empresa = Empresa(nome=nome, tipo=tipo)
        db.session.add(empresa)
        db.session.commit()
        flash("Empresa adicionado", category="success")
        return redirect(url_for('empresa.lista'))

    return render_template("empresa/criar.html")


# Listar produto
@empresa.route('/empresas', methods=['GET', 'POST'])
@login_required
@roles('Admin')
def lista():
    return render_template("empresa/lista.html", empresa=Empresa.query.all())


# Apagar Produto
@empresa.route('/empresa/<int:id>/delete', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def apagar(id):
    empresa = Empresa.query.get_or_404(id)
    if empresa:
        db.session.delete(empresa)
        db.session.commit()
    else:
        flash("Empresa não existe", "error")
    return redirect(url_for('empresa.lista'))


@empresa.route('/empresa/<int:id>/update', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def update(id):
    empresa = Empresa.query.get_or_404(id)
    if request.method == 'POST':
        if empresa:
            empresa.nome = request.form.get('nome')
            empresa.tipo = request.form.get('tipo')

            db.session.commit()
            return redirect(url_for('empresa.lista'))
        flash("Empresa não existe", "error")

    return render_template('empresa/editar.html', data=empresa)
