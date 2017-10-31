from flask_sqlalchemy import SQLAlchemy
from service import app
from flask_security import UserMixin, RoleMixin
 #Create database connection object
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
class Informe(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nro_remitente = db.Column(db.Integer())
	denominacion = db.Column(db.String(1024))
	fecha = db.Column(db.DateTime())
	diasTranscurridos = db.Column(db.Integer())
	tipo_alerta = db.Column(db.String(255))
	estado = db.Column(db.String(255))
	tipo_comprobante = db.Column(db.String(255))
	monto = db.Column(db.String(255))
	fecha_creacion = db.Column(db.DateTime())
	fecha_actualizacion = db.Column(db.DateTime())
	nro_transaccion = db.Column(db.Integer())
	persona_id = db.Column(db.Integer())