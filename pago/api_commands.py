from base import app, api, Pago, pago_schema,  q, Resource, Flask, request
from payment_processor import realizar_pago


class PagosResource(Resource):
    def post(self):
        # TODO: aqui inicia proceso de pago
        # realiza el pago, 
        # graba el registro del pago en la BD
        # retorna si el pago fue procesado o si hubo algun error
        
        data = {
            "client_id": request.json['client_id'],
            "referencia": request.json['referencia'],
            "monto_a_cancelar": request.json['monto_a_cancelar'],
        }

        q.enqueue(realizar_pago, pago_schema.dump(data))
        return {'PagoProcesado': True}

# este endpoint es solo de prueba para hacer que el integrado inicie el pago de un cliente
api.add_resource(PagosResource, '/api-commands/pago')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')