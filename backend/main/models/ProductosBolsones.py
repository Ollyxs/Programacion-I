from .. import db


class BolsonProducto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productoid = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    producto = db.relationship('Producto', back_populates='bolsones')
    bolsonid = db.Column(db.Integer, db.ForeignKey('bolson.id'), nullable=False)
    bolson = db.relationship('Bolson', back_populates='productos')

    def __repr__(self):
        return '<BolsonProducto: %r %r >' % (self.productoid, self.bolsonid)

    def to_json(self):
        bolsonproducto_json = {
            'id': self.id,
            'productoid': self.producto.id,
            'bolsonid': self.bolson.id,
        }
        return bolsonproducto_json

    @staticmethod
    def from_json(bolsonproducto_json):
        id = bolsonproducto_json.get('id')
        productoid = bolsonproducto_json.get('productoid')
        bolsonid = bolsonproducto_json.get('bolsonid')
        return BolsonProducto(id=id,
                              productoid=productoid,
                              bolsonid=bolsonid,
                              )
