import csv
import json
import os
import time
from datetime import datetime

from flask import Blueprint, render_template, request, flash, url_for, redirect, send_file, Response
from flask_login import login_required, current_user

from flask_app import db
from models import Asc, Easc, Variavel, Download, User
from perms import roles

os.environ["MODIN_ENGINE"] = "dask"  # Modin will use Dask

from distributed import Client

client = Client(memory_limit='8GB')
import modin.pandas as dask_pd

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
    qtm = 0
    if dnw:
        qtm = dnw.qtm
        num = dnw.qtd + leads
        asc = Asc.query.filter(Asc.id.between('0', num))
    else:
        asc = Asc.query.filter(Asc.id.between('0', leads))

    dno = Download.query.filter_by(cliente=current_user.id).order_by(Download.data.desc())

    return render_template("movim.html", asc=asc, download=dno, num=num, data=json.dumps(qtm))


@views.route('/download')
@login_required
def download():
    leads = current_user.leads
    idc = current_user.id
    dnw = Download.query.filter_by(cliente=idc).order_by(Download.id.desc()).first()
    if dnw:
        num = dnw.qtd + leads
        qtm = dnw.qtm
        if dnw.desc == False:
            dnr = Download(cliente=idc, data=datetime.now(), qtd=num, qtm=num, desc=True)
        else:
            dnr = Download(cliente=idc, data=datetime.now(), qtm=num)
        asc = Asc.query.filter(Asc.id.between(qtm, num))
    else:
        asc = Asc.query.filter(Asc.id.between('0', leads))
        dnr = Download(cliente=idc, data=datetime.now(), qtm=leads, desc=True)

    # Fazer download do arquivo em csv
    with open('exportar.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(["Nome", "Email", "Telefone"])
        for p in asc:
            csvwriter.writerow([p.nome, p.email, p.tele])

    db.session.add(dnr)
    db.session.commit()
    return send_file('exportar.csv', mimetype='text/csv', attachment_filename='exportar.csv', as_attachment=True,
                     cache_timeout=0)


@views.route('/mudmes')
@login_required
def mudmes():
    dnw = Download.query.all()
    for i in dnw:
        idcli = i.cliente
        usr = User.query.filter_by(id=idcli).first()
        if usr:
            i.qtd = i.qtd + usr.leads
            i.desc = False
    db.session.commit()
    return redirect(url_for('views.movim'))


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
        pais = request.form.get('pais')
        # Adicionar na bd
        if nome == "" or email == "" or tele == "":
            ecount += 1
            elin = Easc(nome=nome, email=email, tele=tele, pais=pais)
            db.session.add(elin)
            db.session.commit()
            flash("Associação incompleta adicionada a tabela de erros", category="error")
        else:
            count += 1
            mov = Asc(nome=nome, email=email, tele=tele, pais=pais)
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
        col_names = ['nome', 'email', 'telefone', 'pais']
        # Use Pandas to parse the CSV file

        csvData = dask_pd.read_csv(file, names=col_names, header=None, decimal=",", keep_default_na=False)
        print("Leu CSV")
        # df = csvData[0].str.split(',', expand=True)
        # csvData = read_csv_in_chunks(file, 5001)
        # Loop through the Rows
        for i, row in csvData.iterrows():
            if row[0] == "" or row[1] == "" or row[2] == "" or row[3] == "":
                ecount += 1
                elin = Easc(nome=row[0], email=row[2], tele=row[1], pais=row[3])
                db.session.add(elin)
                db.session.commit()
            else:
                count += 1
                lin = Asc(nome=row[0], email=row[2], tele=row[1], pais=row[3])
                db.session.add(lin)
                db.session.commit()
            var.count = count
            var.ecount = ecount
            print("Acabou for")
    # db.session.commit()
    return redirect(url_for('views.associacao'))


@views.route('/progress')
def progress():
    def generate():
        x = 0

        while x <= 100:
            yield "data:" + str(x) + "nn"
            x = x + 10
            time.sleep(0.5)

    return Response(generate(), mimetype="text/event-stream")

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
