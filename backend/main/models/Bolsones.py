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
            'productos': self.productos,
        }
        return bolson_json

    @staticmethod
    def from_json(bolson_json):
        try:
            id = bolson_json.get('id')
            nombre = bolson_json.get('nombre')
            aprobado = bolson_json.get('aprobado')
            fecha = datetime.strptime(bolson_json.get('fecha'), formato)
            print(2)
            bolson = Bolson(id=id,
                          nombre=nombre,
                          aprobado=aprobado,
                          fecha=fecha,
                          )
            print(bolson_json)
            if "productos" in bolson_json:
                print(5)
                for productoid in bolson_json.get('productos'):
                    print("producto id", str(productoid))
                    db.session.query(Producto).get_or_404(productoid)
                    bolson.productos.append(BolsonProducto(productoid = productoid))
                    print(7)
            return bolson
            print(4)
        except Exception as error:
            return print(error), 400
