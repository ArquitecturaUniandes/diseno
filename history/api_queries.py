from base import app, api, History, history_schema,  q, Resource, Flask, request


class ClinicalHistoryResource(Resource):
    def get(self, numero_historia):
        obj = History.query.get_or_404(numero_historia)
        return history_schema.dump(obj)


api.add_resource(ClinicalHistoryResource, '/api-queries/history/<int:numero_historia>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

