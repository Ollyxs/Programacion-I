from .. import db
from datetime import datetime


formato = "%Y-%m-%d"


class Bolson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    aprobado = db.Column(db.Boolean, default=False)
    fecha = db.Column(db.DateTime)
    productos = db.relationship('BolsonProducto', back_populates='bolson', cascade='all, delete-orphan')
    compra = db.relationship('Compra', back_populates='bolson', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Bolson: %r %r %r >' % (self.nombre, self.aprobado, self.fecha)

    def to_json(self):
        bolson_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'aprobado': self.aprobado,
            'fecha': str(datetime.strftime(self.fecha, formato)),
        }
        return bolson_json

    @staticmethod
    def from_json(bolson_json):
        try:
            id = bolson_json.get('id')
            nombre = bolson_json.get('nombre')
            aprobado = bolson_json.get('aprobado')
            fecha = datetime.strptime(bolson_json.get('fecha'), formato)
            return Bolson(id=id,
                          nombre=nombre,
                          aprobado=aprobado,
                          fecha=fecha,
                          )
        except Exception:
            return '', 400
