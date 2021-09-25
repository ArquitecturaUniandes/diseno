from api import db
from api import ACL


def add_acl(service, queue, value):
    acl = ACL(service=service, queue=queue, value=value)
    if len(list(ACL.query.filter(ACL.service==service).filter(ACL.queue==queue).all())) == 0:
        db.session.add(acl)
        db.session.commit()

try:
    db.session.remove()
    db.drop_all()
except:
    # fail silently
    pass

db.create_all()

add_acl("reporte_consolidado","q", 0)
add_acl("reporte_financiero","q", 1)
