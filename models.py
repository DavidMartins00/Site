from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    role = db.Column(db.String(150))
    nif = db.Column(db.Integer(), nullable=True)
    tel = db.Column(db.Integer(), nullable=True)
    tempo = db.Column(db.Integer(), default=0)
    tipo = db.Column(db.Integer(), default=0)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    nome = db.Column(db.String(150))
    valor = db.Column(db.Float)
    descr = db.Column(db.String(250))
    foto = db.Column(db.String, nullable=True)
    campanha = db.relationship('Campanha')


class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    tipo = db.Column(db.String(150))
    produto = db.relationship('Produto')
    campanha = db.relationship('Campanha')


class Campanha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    produto = db.Column(db.Integer, db.ForeignKey('produto.id'))
    campanha = db.Column(db.String(150))
    valorcamp = db.Column(db.Float)
    descr = db.Column(db.String(250))
    condicoes = db.Column(db.String(250))
    ofertas = db.Column(db.String(250))
    fotos = db.Column(db.String(250))


class Movim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    email = db.Column(db.String(150))
    tele = db.Column(db.Integer)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
