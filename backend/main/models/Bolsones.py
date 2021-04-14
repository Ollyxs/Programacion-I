from .. import db


class Bolson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    aprobado = db.Column(db.Boolean)
    fecha = db.Column(db.DateTime)

    def __repr__(self):
        return '<Bolson: %r %r %r >' % (self.nombre, self.aprobado, self.fecha)

    def to_json(self):
        bolson_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'aprobado': self.aprobado,
            'fecha': self.date,
        }
        return bolson_json

    @staticmethod
    def from_json(bolson_json):
        id = bolson_json.get('id')
        nombre = bolson_json.get('nombre')
        aprobado = bolson_json.get('aprobado')
        fecha = bolson_json.get('fecha')
        return Bolson(id=id,
                      nombre=nombre,
                      aprobado=aprobado,
                      fecha=fecha
                      )