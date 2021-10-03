import os
import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from redis import Redis
from rq import Queue
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/integrador.db'
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', "secret-jwt")

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
api = Api(app)

# db 0 cola para reporte consolidado
q = Queue(connection=Redis(host='redis', port=6379, db=0))


class InformacionExternaConsolidada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(50), default=datetime.datetime.utcnow)


class InformacionExternaConsolidadaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InformacionExternaConsolidada


informacion_consolidada_schema = InformacionExternaConsolidadaSchema()
