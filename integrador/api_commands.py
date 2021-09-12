from base import app, api, InformacionExternaConsolidada, informacion_consolidada_schema,  q, Resource, Flask, request
from updater import update_reporte_consolidado


class SincronizarDatosResource(Resource):
    def post(self):
        cita_id = request.json['cita_id']
        # TODO: aqui inicia proceso de consolidado
        # llama a servicios externos y graba en InformacionExternaConsolidada
        data = InformacionExternaConsolidada.query.get_or_404(cita_id)
        # data = [{"cita_id":1},{"cita_id":2},{"cita_id":3}]

        q.enqueue(update_reporte_consolidado, informacion_consolidada_schema.dump(data))
        return {'Sincronizando': True}

# este endpoint es solo de prueba para hacer que el integrado inicie la consolidacion de una cita
api.add_resource(SincronizarDatosResource, '/api-commands/integrador')


class EstadoDeSaludResource(Resource):
    def get(self):
        '{"estado": "ok"}', 200

api.add_resource(EstadoDeSaludResource, '/estado-de-salud')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
