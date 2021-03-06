from base import app, api, History, history_schema,  q, Resource, Flask, request
from updater import history_user_update
from flask_jwt_extended import jwt_required


class ClinicalHistoryResource(Resource):
    @jwt_required()
    def post(self):
        # TODO: Init Clinical History
        # Search the clinical history, 
        # Save the clinical history
        # return true or false if the history clinical was succesfully submited
        
        data = {
            "client_id": request.json['client_id'],
            "numero_historia": request.json['numero_historia'],
            "nombre_usuario": request.json['nombre_usuario'],
            "descripcion_usuario": request.json['descripcion_usuario'],
            "plan_tratamiento": request.json['plan_tratamiento'],
            "recomendaciones_usuario": request.json['recomendaciones_usuario'],
        }

        q.enqueue(history_user_update, history_schema.dump(data))
        return {'ClinicalHistory': True}

# testing endpoint
api.add_resource(ClinicalHistoryResource, '/api-commands/history')


class EstadoDeSaludResource(Resource):
    def get(self):
        '{"estado": "ok"}', 200

api.add_resource(EstadoDeSaludResource, '/estado-de-salud')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
    