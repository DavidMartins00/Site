from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from models import Movim, Easc
from flask_app import db
from perms import roles
import pandas as pd

views = Blueprint('views', __name__)

ecount = 0
count = 0


@views.route('/')
@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@views.route('/associacao', methods=['GET', 'POST'])
# @login_required
def associacao():
    global count, ecount
    if request.method == 'POST':
        # Ir buscar dados ao html
        nome = request.form.get('nome')
        email = request.form.get('email')
        tele = request.form.get('tele')
        # Adicionar na bd
        if nome == "" or email == "" or tele == "":
            ecount += 1
            elin = Easc(nome=nome, email=email, tele=tele)
            db.session.add(elin)
            db.session.commit()
            flash("Associação incompleta adicionada a tabela de erros", category="error")
        else:
            count += 1
            mov = Movim(nome=nome, email=email, tele=tele)
            db.session.add(mov)
            db.session.commit()
            flash("Associação Adicionada", category="success")

        return redirect(url_for('views.associacao'))
    return render_template("asc.html", movi=Movim.query.all(), er=Easc.query.all(), cnt=count, ecnt=ecount)


@views.route('/uploadcsv', methods=['GET', 'POST'])
# @login_required
def uploadcsv():
    global count, ecount
    if request.method == 'POST':
        count = 0
        file = request.files['file']
        # CVS Column Names
        col_names = ['nome', 'email', 'telefone']
        # Use Pandas to parse the CSV file
        csvData = pd.read_csv(file, names=col_names, header=None, decimal=",", keep_default_na=False)
        # Loop through the Rows
        for i, row in csvData.iterrows():
            if row[2] == "email" or row[2] == "Email" or row[2] == "EMAIL":
                pass
            elif row[0] == "" or row[1] == "" or row[2] == "":
                ecount += 1
                elin = Easc(nome=row[0], email=row[2], tele=row[1])
                db.session.add(elin)
                db.session.commit()
            else:
                count += 1
                lin = Movim(nome=row[0], email=row[2], tele=row[1])
                db.session.add(lin)
                db.session.commit()
        return redirect(url_for('views.associacao'))
    else:
        flash("Erro no ficheiro", "error")


@views.route('/asc/<int:id>/update', methods=['GET', 'POST'])
# @login_required
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


@views.route('/easc/<int:id>/update', methods=['GET', 'POST'])
# @login_required
def eupdate(id):
    emov = Easc.query.get_or_404(id)
    if request.method == 'POST':
        if emov:
            nome = request.form.get('nome')
            email = request.form.get('email')
            tele = request.form.get('tele')
            if nome != "" and email != "" and tele != "":
                # Adicionar na bd
                mov = Movim(nome=nome, email=email, tele=tele)
                db.session.add(mov)
                db.session.delete(emov)
                db.session.commit()
                return redirect(url_for('views.associacao'))
        flash("Dados não existem", "error")
    return render_template('easc.html', data=emov)
