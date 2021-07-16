from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from os.path import join, dirname, realpath

from sqlalchemy import create_engine

db = SQLAlchemy()
DB_NAME = "database.db"
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NSKCSDdas'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from views import views
from auth import auth
from users import user
from produtos import produto
from empresas import empresa
from campanhas import campanha
from clientes import cli

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(user, url_prefix='/')
app.register_blueprint(produto, url_prefix='/')
app.register_blueprint(empresa, url_prefix='/')
app.register_blueprint(campanha, url_prefix='/')
app.register_blueprint(cli, url_prefix='/')

from models import User

# Criar base de dados
if not path.exists('site/' + DB_NAME):
    db.create_all(app=app)

#####################
# Timer para mudar os a quantidade de arquivos que o cliente pode baixar
# (Não funciona)
# import timer
# timer.start()
#####################

# Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
login_manager.login_message = "Por favor, faça login para acessar a esta pagina."
login_manager.login_message_category = "error"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


if __name__ == '__main__':
    app.run(debug=True)
