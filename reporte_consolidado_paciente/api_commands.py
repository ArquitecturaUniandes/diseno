from base import app, api, ma, db, ReporteConsolidado, reporte_consolidado_schema, Resource, Flask, request
import requests
import json

class ReporteConsolidadoResource(Resource):
    def post(self):
        pago_examen_a = {
            "client_id":1,
            "referencia": "examen a del cliente",
            "monto_a_cancelar": 1000
        }
        pago_examen_b = {
            "client_id":1,
            "referencia": "examen b del cliente",
            "monto_a_cancelar": 2000
        }
        pago_examen_c = {
            "client_id":1,
            "referencia": "examen c del cliente",
            "monto_a_cancelar": 3000
        }
        # datos_de_pago = {
        #     "client_id":1,
        #     "referencia": "cliente numero 1",
        #     "monto_a_cancelar": 1000
        # }
        confirmacion_de_pagos_a = requests.post('http://pago-commands:5000/api-commands/pago',json=pago_examen_a)
        confirmacion_de_pagos_b = requests.post('http://pago-commands:5000/api-commands/pago',json=pago_examen_b)
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
