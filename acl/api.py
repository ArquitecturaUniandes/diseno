import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////backend/acl.db'
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', "secret-jwt")

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
api = Api(app)


class ACL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    service = db.Column(db.String(50))
    queue = db.Column(db.String(50))



class ACLSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("value",)


ACL_schema = ACLSchema()

class ACLResource(Resource):
    @jwt_required()
    def get(self, service_name, queue_name):
        acl = ACL.query.filter(ACL.service==service_name).filter(ACL.queue==queue_name).first_or_404()
        return ACL_schema.dump(acl)


api.add_resource(ACLResource, '/api-queries/acl/<string:service_name>/<string:queue_name>')


class EstadoDeSaludResource(Resource):
    def get(self):
        '{"estado": "ok"}', 200

api.add_resource(EstadoDeSaludResource, '/estado-de-salud')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')