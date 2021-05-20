from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from models import Movim
from flask_app import db
from perms import roles
from io import TextIOWrapper
import csv

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@views.route('/associacao', methods=['GET', 'POST'])
@login_required
def associacao():
    if request.method == 'POST':
        # Ir buscar dados ao html
        nome = request.form.get('nome')
        email = request.form.get('email')
        tele = request.form.get('tele')

        # Adicionar na bd
        mov = Movim(nome=nome, email=email, tele=tele)
        db.session.add(mov)
        db.session.commit()
        flash("Associação Adicionada", category="success")
        return redirect(url_for('views.associacao'))

    return render_template("asc.html", movi=Movim.query.all())


@views.route('/uploadcsv', methods=['GET', 'POST'])
@login_required
def uploadcsv():
    if request.method == 'POST':
        csv_file = request.files['file']
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            lin = Movim(nome=row[0], email=row[1], tele=row[2])
            db.session.add(lin)
            db.session.commit()
        return redirect(url_for('views.associacao'))
    else:
        flash("Erro no ficheiro", "error")


@views.route('/asc/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    mov = Movim.query.get_or_404(id)
    if request.method == 'POST':
        if mov:
            mov.nome = request.form.get('nome')
            mov.email = request.form.get('email')
            mov.tele = request.form.get('tele')

            db.session.commit()
            return redirect(url_for('views.associacao'))
        flash("Dados não existem", "error")

    return render_template('easc.html', data=mov)
