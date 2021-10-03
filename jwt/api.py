import datetime
import os
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', "secret-jwt")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(seconds=60)

jwt = JWTManager(app)
api = Api(app)

class AuthResource(Resource):
    def get(self):
        role_type = request.args.get('type', None)
        token_data = {
            "identity": "test"
        }

        if role_type == 'funcionario':
            token_data["additional_claims"] = {"is_funcionario": True}
        elif role_type == 'paciente':
            token_data["additional_claims"] = {"is_paciente": True}
        elif role_type == 'contador':
            token_data["additional_claims"] = {"is_contador": True}
        elif role_type == 'queue_manager':
            token_data["additional_claims"] = {"is_queue_manager": True}            
        else:
            token_data["additional_claims"] = {"is_anonymous": True}

        access_token = create_access_token(**token_data)
        return jsonify(access_token=access_token)


api.add_resource(AuthResource, '/api-queries/jwt')


class EstadoDeSaludResource(Resource):
    def get(self):
        '{"estado": "ok"}', 200

api.add_resource(EstadoDeSaludResource, '/estado-de-salud')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')