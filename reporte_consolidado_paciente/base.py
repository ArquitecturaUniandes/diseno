import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from redis import Redis
from rq import Queue


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/reporte_consolidado_paciente.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

# db 0 cola para reporte consolidado
q = Queue(connection=Redis(host='redis', port=6379, db=0))


class ReporteConsolidado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(50), default=datetime.datetime.utcnow)


class ReporteConsolidadoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ReporteConsolidado


reporte_consolidado_schema = ReporteConsolidadoSchema()
reportes_consolidado_schema = ReporteConsolidadoSchema(many=True)
