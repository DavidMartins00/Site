import shutil
from flask import Blueprint, render_template, request, flash, url_for, redirect, send_from_directory
from flask_login import login_required
from models import Produto, Empresa, Campanha
from flask_app import db
from perms import roles
import os
import random
from flask_app import app

produto = Blueprint('produto', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

        # FOTO
        foto = str(random.randrange(1, 9223372036854775807))

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        fol = app.config['UPLOAD_FOLDER']

        fol += "/" + foto
        os.mkdir(fol)
        temp = 1
        for file in files:
            if file and allowed_file(file.filename):
                filename = str(temp) + "." + "jpg"
                temp += 1
                file.save(os.path.join(fol, filename))
            # -----Foto------
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
        path = "static/uploads/"+produto.foto
        if os.path.exists(path):
            # removing the file using the os.remove() method
            shutil.rmtree(path)
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
            if not request.form.get('foto') == "":
                foto = str(random.randrange(1, 9223372036854775807))
                files = request.files.getlist('files[]')
                fol = app.config['UPLOAD_FOLDER']
                #Apagar diretorio anterior
                path = "static/uploads/" + produto.foto
                if os.path.exists(path):
                    # removing the file using the os.remove() method
                    shutil.rmtree(path)
                fol += "/" + foto
                os.mkdir(fol)
                temp = 1
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = str(temp) + "." + "jpg"
                        temp += 1
                        file.save(os.path.join(fol, filename))
                        produto.foto = foto
                        print(foto)
            db.session.commit()
            return redirect(url_for('produto.lista'))
        flash("Produto não existe", "error")

    return render_template('produto/editar.html', data=produto, empresa=Empresa.query.all())


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
