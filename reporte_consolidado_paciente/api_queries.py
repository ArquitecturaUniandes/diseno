from base import app, api, ma, db, ReporteConsolidado, reporte_consolidado_schema, q, Resource, Flask, request
from permissions import funcionario_required


class ReporteConsolidadoResource(Resource):
    @funcionario_required()
    def get(self, consolidado_id):
        obj = ReporteConsolidado.query.get_or_404(consolidado_id)
        return reporte_consolidado_schema.dump(obj)


api.add_resource(ReporteConsolidadoResource, '/api-queries/reporte-consolidado/<int:consolidado_id>')


class EstadoDeSaludResource(Resource):
    def get(self):
        '{"estado": "ok"}', 200

api.add_resource(EstadoDeSaludResource, '/estado-de-salud')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
