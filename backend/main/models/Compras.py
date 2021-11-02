from .. import db
from . import UsuarioModel
from datetime import datetime


class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clienteid = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    cliente = db.relationship('Usuario', back_populates='compra', uselist=False, single_parent=True)
    bolsonid = db.Column(db.Integer, db.ForeignKey('bolson.id'), nullable=False)
    bolson = db.relationship('Bolson', back_populates='compra', uselist=False, single_parent=True)
    fechaHoraCompra = db.Column(db.DateTime, default=datetime.now)
    retirado = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Compra: %r %r %r %r >' % (self.clienteid, self.bolsonid, self.fechaHoraCompra, self.retirado)

    def to_json(self):
        compra_json = {
            'id': self.id,
            'cliente': self.cliente.nombre + ' ' + self.cliente.apellido,
            'bolson': self.bolson.nombre,
            'fechaHoraCompra': str(self.fechaHoraCompra),
            'retirado': self.retirado,
            'precio': self.bolson.precio
        }
        return compra_json

    @staticmethod
    def from_json(compra_json):
        id = compra_json.get('id')
        clienteid = compra_json.get('clienteid')
        bolsonid = compra_json.get('bolsonid')
        fechaHoraCompra = compra_json.get('fechaHoraCompra')
        retirado = compra_json.get('retirado')
        return Compra(id=id,
                      clienteid=clienteid,
                      bolsonid=bolsonid,
                      fechaHoraCompra=fechaHoraCompra,
                      retirado=retirado,
                      )
