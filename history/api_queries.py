from base import app, api, History, history_schema,  q, Resource, Flask, request
from flask_jwt_extended import jwt_required


class ClinicalHistoryResource(Resource):
    @jwt_required()
    def get(self, numero_historia):
        obj = History.query.get_or_404(numero_historia)
        return history_schema.dump(obj)


api.add_resource(ClinicalHistoryResource, '/api-queries/history/<int:numero_historia>')


class EstadoDeSaludResource(Resource):
    def get(self):
        '{"estado": "ok"}', 200

api.add_resource(EstadoDeSaludResource, '/estado-de-salud')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')

