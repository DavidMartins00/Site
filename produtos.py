from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required
from models import Produto, Empresa, Campanha
from flask_app import db
from perms import roles

produto = Blueprint('produto', __name__)


# Adicionar Produto
@produto.route('/addproduto', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def criar():
    if request.method == 'POST':
        # Ir buscar dados ao html
        empresa = request.form.get('empresa')
        nome = request.form.get('nome')
        valor = request.form.get('valor')
        descr = request.form.get('descr')
        foto = request.form.get('foto')

        # Adicionar na bd
        produto = Produto(empresa=empresa, nome=nome, valor=valor, descr=descr, foto=foto)
        db.session.add(produto)
        db.session.commit()
        flash("Produto adicionado", category="success")

        return redirect(url_for('produto.lista'))

    return render_template("produto/criar.html", empresa=Empresa.query.all(), campanha=Campanha.query.all())


# Listar produto
@produto.route('/produtos', methods=['GET', 'POST'])
@login_required
@roles('Admin')
def lista():
    return render_template("produto/lista.html", produto=Produto.query.all(), empresa=Empresa.query.all())


# Apagar Produto
@produto.route('/produto/<int:id>/delete', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def apagar(id):
    produto = Produto.query.get_or_404(id)
    if produto:
        db.session.delete(produto)
        db.session.commit()
    else:
        flash("Produto não existe", "error")
    return redirect(url_for('produto.lista'))


@produto.route('/produto/<int:id>/update', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def update(id):
    produto = Produto.query.get_or_404(id)
    if request.method == 'POST':
        if produto:
            produto.empresa = request.form.get('empresa')
            produto.nome = request.form.get('nome')
            produto.valor = request.form.get('valor')
            produto.descr = request.form.get('descr')
            produto.foto = request.form.get('foto')

            db.session.commit()
            return redirect(url_for('produto.lista'))
        flash("Produto não existe", "error")

    return render_template('produto/editar.html', data=produto, empresa=Empresa.query.all())
