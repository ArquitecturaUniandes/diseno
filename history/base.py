import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from redis import Redis
from rq import Queue


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/history.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

q = Queue(connection=Redis(host='redis', port=6379, db=2))


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer)
    numero_historia = db.Column(db.Integer)
    nombre_usuario = db.Column(db.String)
    descripcion_usuario = db.Column(db.String)
    plan_tratamiento = db.Column(db.String)
    recomendaciones_usuario = db.Column(db.String)
    created_at = db.Column(db.DateTime(50), default=datetime.datetime.utcnow)


class HistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = History


history_schema = HistorySchema()

