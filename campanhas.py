import os
import random
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required
from models import Campanha, Produto, Empresa
from flask_app import db, app
from perms import roles

campanha = Blueprint('campanha', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Adicionar Produto
@campanha.route('/addcampanha', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def criar():
    if request.method == 'POST':
        # Ir buscar dados ao html
        empresa = request.form.get('empresa')
        produto = request.form.get('produto')
        campanha = request.form.get('campanha')
        valorcamp = request.form.get('valorcamp')
        descr = request.form.get('descr')
        condicoes = request.form.get('condicoes')
        ofertas = request.form.get('ofertas')
        fotos = request.form.get('fotos')

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
        campanha = Campanha(empresa=empresa, produto=produto, campanha=campanha, valorcamp=valorcamp, descr=descr,
                            condicoes=condicoes, ofertas=ofertas, fotos=foto)
        db.session.add(campanha)
        db.session.commit()
        flash("Campanha adicionado", category="success")
        return redirect(url_for('campanha.lista'))

    return render_template("campanha/criar.html", empresa=Empresa.query.all(), produto=Produto.query.all())


# Listar produto
@campanha.route('/campanhas', methods=['GET', 'POST'])
@login_required
@roles('Admin')
def lista():
    return render_template("campanha/lista.html", campanha=Campanha.query.all(), produto=Produto.query.all(), empresa=Empresa.query.all())


# Apagar Produto
@campanha.route('/campanha/<int:id>/delete', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def apagar(id):
    campanha = Campanha.query.get_or_404(id)
    if campanha:
        db.session.delete(campanha)
        db.session.commit()
    else:
        flash("Campanha não existe", "error")
    return redirect(url_for('campanha.lista'))


@campanha.route('/campanha/<int:id>/update', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def update(id):
    campanha = Campanha.query.get_or_404(id)
    if request.method == 'POST':
        if campanha:
            campanha.empresa = request.form.get('empresa')
            campanha.produto = request.form.get('produto')
            campanha.campanha = request.form.get('campanha')
            campanha.valorcamp = request.form.get('valorcamp')
            campanha.descr = request.form.get('descr')
            campanha.condicoes = request.form.get('condicoes')
            campanha.ofertas = request.form.get('ofertas')
            if not request.form.get('foto') == "":
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
                        campanha.fotos = foto

            db.session.commit()
            return redirect(url_for('campanha.lista'))
        flash("Campanha não existe", "error")

    return render_template('campanha/editar.html', data=campanha, empresa=Empresa.query.all(), produto=Produto.query.all())
