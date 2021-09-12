import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from redis import Redis
from rq import Queue


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////backend/monitor.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

# db 0 cola para reporte consolidado
#q = Queue(connection=Redis(host='redis', port=6379, db=0))


class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    health_check_uri = db.Column(db.String(150))
    created_at = db.Column(db.DateTime(50), default=datetime.datetime.utcnow)


class ServicioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Servicio


servicio_schema = ServicioSchema()
