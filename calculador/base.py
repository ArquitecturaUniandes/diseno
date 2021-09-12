import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from redis import Redis
from rq import Queue

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/calculador.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

q = Queue(connection=Redis(host='redis', port=6379, db=3))


class Calculador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer)
    suma_total_monto_a_cancelar = db.Column(db.Float)
    created_at = db.Column(db.DateTime(50), default=datetime.datetime.utcnow)


class CalculadorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Calculador


calculador_schema = CalculadorSchema()