import csv
from datetime import datetime

from flask import Blueprint, render_template, request, flash, url_for, redirect, send_file
from flask_login import login_required, current_user
from models import Asc, Easc, Variavel, Download
from flask_app import db
from perms import roles
import pandas as pd
from datetime import date

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@views.route('/movimentacao')
@login_required
def movim():
    dnw = Download.query.filter_by(cliente=current_user.id).order_by(Download.data.desc()).first()
    leads = current_user.leads
    num = 0
    if dnw:
        num = dnw.qtd + leads
        asc = Asc.query.filter(Asc.id.between('0', num))
    else:
        asc = Asc.query.filter(Asc.id.between('0', leads))

    dno = Download.query.filter_by(cliente=current_user.id).order_by(Download.data.desc())

    return render_template("movim.html", asc=asc, download=dno, num=num)


@views.route('/download')
def download():
    leads = current_user.leads
    idc = current_user.id
    dnw = Download.query.filter_by(cliente=idc).order_by(Download.id.desc()).first()
    if dnw:
        num = dnw.qtd + leads
        asc = Asc.query.filter(Asc.id.between(dnw.qtd, num))
        dnr = Download(cliente=idc, data=datetime.now(), qtd=dnw.qtd)
    else:
        asc = Asc.query.filter(Asc.id.between('0', leads))
        dnr = Download(cliente=idc, data=datetime.now(), qtd=leads)

    # Fazer download do arquivo em csv
    with open('exportar.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(["Nome", "Email", "Telefone"])
        for p in asc:
            csvwriter.writerow([p.nome, p.email, p.tele])

    db.session.add(dnr)
    db.session.commit()
    return send_file('exportar.csv', mimetype='text/csv', attachment_filename='exportar.csv', as_attachment=True)


@views.route('/associacao', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def associacao():
    var = Variavel.query.get(1)
    if not var:
        var = Variavel(count=0, ecount=0)
        db.session.add(var)
        db.session.commit()
    count = var.count
    ecount = var.ecount
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
            mov = Asc(nome=nome, email=email, tele=tele)
            db.session.add(mov)
            db.session.commit()
            flash("Associação Adicionada", category="success")
        var.count = count
        var.ecount = ecount
        db.session.commit()
        return redirect(url_for('views.associacao'))
    return render_template("asc.html", movi=Asc.query.all(), er=Easc.query.all(), var=Variavel.query.get(1))


@views.route('/uploadcsv', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def uploadcsv():
    var = Variavel.query.get(1)
    count = var.count
    ecount = var.ecount
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
                lin = Asc(nome=row[0], email=row[2], tele=row[1])
                db.session.add(lin)
                db.session.commit()
            var.count = count
            var.ecount = ecount
            db.session.commit()
        return redirect(url_for('views.associacao'))
    else:
        flash("Erro no ficheiro", "error")


@views.route('/asc/<int:id>/update', methods=['GET', 'POST'])
@login_required
@roles("Admin")
def update(id):
    mov = Asc.query.get_or_404(id)
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
@login_required
@roles("Admin")
def eupdate(id):
    emov = Easc.query.get_or_404(id)
    if request.method == 'POST':
        if emov:
            nome = request.form.get('nome')
            email = request.form.get('email')
            tele = request.form.get('tele')
            if nome != "" and email != "" and tele != "":
                # Adicionar na bd
                mov = Asc(nome=nome, email=email, tele=tele)
                db.session.add(mov)
                db.session.delete(emov)
                db.session.commit()
                return redirect(url_for('views.associacao'))
        flash("Dados não existem", "error")
    return render_template('easc.html', data=emov)
