import os
import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from redis import Redis
from rq import Queue
from flask_jwt_extended import JWTManager
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/reporte_consolidado_paciente.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', "secret-jwt")

jwt = JWTManager(app)

api = Api(app)

# db 0 cola para reporte consolidado
token = requests.get(f"https://jwt-queries:5000/api-queries/jwt?type=queue_manager", verify=False)
token = token.json()
headers = {'Authorization': f"Bearer {token['access_token']}"}

# queue_name = None
try:
    queue_name = requests.get(f"https://acl-queries:5000/api-queries/acl/reporte_consolidado/q", verify=False, headers=headers)    
    queue_name = queue_name.json()
    queue_name = queue_name['value']
except:
    print("Queue q not in ACL for Service orders")
    exit(1)

q = Queue(connection=Redis(host='redis', port=6379, db=queue_name))


class ReporteConsolidado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(50), default=datetime.datetime.utcnow)


class ReporteConsolidadoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ReporteConsolidado


reporte_consolidado_schema = ReporteConsolidadoSchema()
reportes_consolidado_schema = ReporteConsolidadoSchema(many=True)
