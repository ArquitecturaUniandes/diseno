from base import app, api, ma, db, ReporteConsolidado, reporte_consolidado_schema, q, Resource, Flask, request


class ReporteConsolidadoResource(Resource):
    def get(self, consolidado_id):
        obj = ReporteConsolidado.query.get_or_404(consolidado_id)
        return reporte_consolidado_schema.dump(obj)


api.add_resource(ReporteConsolidadoResource, '/api-queries/reporte-consolidado/<int:consolidado_id>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
