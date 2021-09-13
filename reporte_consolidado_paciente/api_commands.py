from base import app, api, ma, db, ReporteConsolidado, reporte_consolidado_schema, Resource, Flask, request
import requests
import json

class ReporteConsolidadoResource(Resource):
    def post(self):
        monto_examen_a = 1000
        monto_examen_b = 2000
        monto_examen_c = 3000
        client_id = 1

        calculo_examen_a = {
            "client_id": client_id,
            "suma_total_monto_a_cancelar": monto_examen_a
        }
        pago_examen_a = {
            "client_id": client_id,
            "referencia": "examen a del cliente",
            "monto_a_cancelar": monto_examen_a
        }
        calculo_examen_b = {
            "client_id": client_id,
            "suma_total_monto_a_cancelar": monto_examen_b
        }
        pago_examen_b = {
            "client_id": client_id,
            "referencia": "examen b del cliente",
            "monto_a_cancelar": monto_examen_b
        }
        calculo_examen_c = {
            "client_id": client_id,
            "suma_total_monto_a_cancelar": monto_examen_c
        }
        pago_examen_c = {
            "client_id": client_id,
            "referencia": "examen c del cliente",
            "monto_a_cancelar": monto_examen_c
        }
        # datos_de_pago = {
        #     "client_id":1,
        #     "referencia": "cliente numero 1",
        #     "monto_a_cancelar": 1000
        # }
        calculo_de_pagos_a = requests.post('http://calculador-commands:5000/api-commands/calculador',json=calculo_examen_a)
        confirmacion_de_pagos_a = requests.post('http://pago-commands:5000/api-commands/pago',json=pago_examen_a)
        calculo_de_pagos_b = requests.post('http://calculador-commands:5000/api-commands/calculador',json=calculo_examen_b)
        confirmacion_de_pagos_b = requests.post('http://pago-commands:5000/api-commands/pago',json=pago_examen_b)
        calculo_de_pagos_c = requests.post('http://calculador-commands:5000/api-commands/calculador',json=calculo_examen_c)
        confirmacion_de_pagos_c = requests.post('http://pago-commands:5000/api-commands/pago',json=pago_examen_c)
        if confirmacion_de_pagos_a.status_code != 200:
            return {"pago": "no se pudo procesar confirmacion de pago a"}, 400
        if confirmacion_de_pagos_b.status_code != 200:
            return {"pago": "no se pudo procesar confirmacion de pago b"}, 400
        if confirmacion_de_pagos_c.status_code != 200:
            return {"pago": "no se pudo procesar confirmacion de pago c"}, 400
        obj = ReporteConsolidado()
        db.session.add(obj)
        db.session.commit()
        # TODO: llama a calculador
        return reporte_consolidado_schema.dump(obj)


api.add_resource(ReporteConsolidadoResource, '/api-commands/reporte-consolidado')


class EstadoDeSaludResource(Resource):
    def get(self):
        '{"estado": "ok"}', 200

api.add_resource(EstadoDeSaludResource, '/estado-de-salud')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
