from service import app,queries
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from service import app,tablas
 #Create database connection object

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(tablas.db, tablas.User, tablas.Role)
security = Security(app, user_datastore)


# Views
@app.route('/')
@login_required
def home():
    return queries.graficos()

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    return queries.subirArchivos()
@app.route('/datos')
@login_required
def datos():
    return queries.datos
@app.route('/tablas')
@login_required
def tablas():
    return queries.tablas()