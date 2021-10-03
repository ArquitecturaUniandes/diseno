from base import db, Servicio


def add_service(service, health_check_uri):
    service = Servicio(name=service, health_check_uri=health_check_uri)    
    db.session.add(service)
    db.session.commit()

try:
    db.session.remove()
    db.drop_all()
except:
    # fail silently
    pass

db.create_all()

add_service("integrador-commands", "estado-de-salud")
add_service("reporte_consolidado_paciente-queries", "estado-de-salud")
add_service("reporte_consolidado_paciente-commands", "estado-de-salud")
add_service("pago-commands", "estado-de-salud")
add_service("clinical_history-commands", "estado-de-salud")
add_service("clinical_history-queries", "estado-de-salud")
#add_service("worker-reporte_consolidado_paciente", "estado-de-salud")
add_service("calculador-commands", "estado-de-salud")
add_service("reporte_financiero-queries", "estado-de-salud")
add_service("reporte_financiero-commands", "estado-de-salud")
add_service("acl-queries", "estado-de-salud")
add_service("jwt-queries", "estado-de-salud")