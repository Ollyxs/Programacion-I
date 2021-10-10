from .. import db


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(1000), nullable=False)
    proveedorid = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    proveedor = db.relationship('Usuario', back_populates='productos', uselist=False, single_parent=True)
    bolsones = db.relationship('BolsonProducto', back_populates='producto', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Producto: %r %r >' % (self.nombre, self.proveedorid)

    def to_json(self):
        producto_json = {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'proveedor': self.proveedor.nombre + ' ' + self.proveedor.apellido,
        }
        return producto_json

    @staticmethod
    def from_json(producto_json):
        id = producto_json.get('id')
        nombre = producto_json.get('nombre')
        descripcion = producto_json.get('descripcion')
        proveedorid = producto_json.get('proveedorid')
        return Producto(id=id,
                        nombre=nombre,
                        descripcion=descripcion,
                        proveedorid=proveedorid,
                        )
