from base import db, InformacionExternaConsolidada
db.create_all()

l1 = InformacionExternaConsolidada(id =1, cita_id =1)
l2 = InformacionExternaConsolidada(id =2, cita_id =2)

db.session.add(l1)
db.session.add(l2)

db.session.commit()

