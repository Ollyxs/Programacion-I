from .. import db


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    proveedorid = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Producto: %r %r >' % (self.nombre, self.proveedorid)

    def to_json(self):
        producto_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'proveedorid': self.proveedorid,
        }
        return producto_json

    @staticmethod
    def from_json(producto_json):
        id = producto_json.get('id')
        nombre = producto_json.get('nombre')
        proveedorid = producto_json.get('proveedorid')
        return Producto(id=id,
                        nombre=nombre,
                        proveedorid=proveedorid,
                        )
