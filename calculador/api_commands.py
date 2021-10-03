from base import app, api, Calculador, calculador_schema,  q, Resource, Flask, request
from reporte_calculos import suma_total_monto_a_cancelar
from flask_jwt_extended import jwt_required
from permissions import funcionario_required


class CalculoResource(Resource):
    @funcionario_required()
    def post(self):
        # TODO: aqui inicia proceso de pago
        # realiza el pago, 
        # graba el registro del pago en la BD
        # retorna si el pago fue procesado o si hubo algun error
        
        data = {
            "client_id": request.json['client_id'],
            "suma_total_monto_a_cancelar": request.json['suma_total_monto_a_cancelar'],
        }

        q.enqueue(suma_total_monto_a_cancelar, calculador_schema.dump(data))
        return {'Total Monto a Cancelar Calculado': True}

# este endpoint es solo de prueba para hacer que el integrado inicie el pago de un cliente
api.add_resource(CalculoResource, '/api-commands/calculador')


class EstadoDeSaludResource(Resource):
    def get(self):
        '{"estado": "ok"}', 200

api.add_resource(EstadoDeSaludResource, '/estado-de-salud')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')