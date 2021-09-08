from base import app, api, ma, db, ReporteConsolidado, reporte_consolidado_schema, Resource, Flask, request


class ReporteConsolidadoResource(Resource):
    def post(self):
        obj = ReporteConsolidado()
        db.session.add(obj)
        db.session.commit()
        # TODO: llama a calculador
        return reporte_consolidado_schema.dump(obj)


api.add_resource(ReporteConsolidadoResource, '/api-commands/reporte-consolidado')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
