from .. import db
from datetime import datetime
from main.models.ProductosBolsones import BolsonProducto
from main.models.Productos import Producto

formato = "%Y-%m-%d"


class Bolson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    aprobado = db.Column(db.Boolean, default=False)
    fecha = db.Column(db.DateTime)
    precio = db.Column(db.Float, nullable=False)
    productos = db.relationship('BolsonProducto', back_populates='bolson', cascade='all, delete-orphan')
    compra = db.relationship('Compra', back_populates='bolson', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Bolson: %r %r %r %r >' % (self.nombre, self.aprobado, self.fecha, self.precio)

    def to_json(self):
        productos = [producto.to_json() for producto in self.productos]
        bolson_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'aprobado': self.aprobado,
            'fecha': str(datetime.strftime(self.fecha, formato)),
            'precio': self.precio,
            'productos': productos,
        }
        return bolson_json

    @staticmethod
    def from_json(bolson_json):
        try:
            id = bolson_json.get('id')
            nombre = bolson_json.get('nombre')
            aprobado = bolson_json.get('aprobado')
            fecha = datetime.strptime(bolson_json.get('fecha'), formato)
            precio =bolson_json.get('precio')
            bolson = Bolson(id=id,
                          nombre=nombre,
                          aprobado=aprobado,
                          fecha=fecha,
                          precio=precio
                          )
            if "productos" in bolson_json:
                for productoid in bolson_json.get('productos'):
                    print("producto id", str(productoid))
                    producto = db.session.query(Producto).get(productoid)
                    if producto:
                        bolson.productos.append(BolsonProducto(productoid = productoid))
                    else:
                        raise Exception("Producto no válido")
            return bolson
        except Exception as error:
            return str(error)
