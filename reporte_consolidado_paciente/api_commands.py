from base import app, api, ma, db, ReporteConsolidado, reporte_consolidado_schema, Resource, Flask, request
import requests
import json
#from flask_jwt_extended import jwt_required
from permissions import funcionario_required


class ReporteConsolidadoResource(Resource):
    @funcionario_required()
    def post(self):
        print('###############ReporteConsolidadoResource')
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
        token = requests.get(f"https://jwt-queries:5000/api-queries/jwt?type=funcionario", verify=False)
        token = token.json()
        headers = {'Authorization': f"Bearer {token['access_token']}"}

        calculo_de_pagos_a = requests.post('https://calculador-commands:5000/api-commands/calculador', headers=headers, json=calculo_examen_a, verify=False)
        confirmacion_de_pagos_a = requests.post('https://pago-commands:5000/api-commands/pago', headers=headers, json=pago_examen_a, verify=False)
        calculo_de_pagos_b = requests.post('https://calculador-commands:5000/api-commands/calculador', headers=headers, json=calculo_examen_b, verify=False)
        confirmacion_de_pagos_b = requests.post('https://pago-commands:5000/api-commands/pago', headers=headers, json=pago_examen_b, verify=False)
        calculo_de_pagos_c = requests.post('https://calculador-commands:5000/api-commands/calculador', headers=headers, json=calculo_examen_c, verify=False)
        confirmacion_de_pagos_c = requests.post('https://pago-commands:5000/api-commands/pago', headers=headers, json=pago_examen_c, verify=False)
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
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
