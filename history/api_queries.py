from base import app, api, History, history_schema,  q, Resource, Flask, request


class ClinicalHistoryResource(Resource):
    def get(self, consolidado_id):
        obj = ClinicalHistory.query.get_or_404(numero_historia)
        return history_schema.dump(obj)


api.add_resource(ClinicalHistoryResource, '/api-queries/clinical-history/<int:numero_historia>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

