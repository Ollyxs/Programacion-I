from .. import db


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    compra = db.relationship('Compra', back_populates='cliente', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Cliente %r %r %r %r >' % (self.nombre, self.apellido, self.telefono, self.email)

    def to_json(self):
        cliente_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'apellido': str(self.apellido),
            'telefono': str(self.telefono),
            'email': str(self.email),
        }
        return cliente_json

    @staticmethod
    def from_json(cliente_json):
        id = cliente_json.get('id')
        nombre = cliente_json.get('nombre')
        apellido = cliente_json.get('apellido')
        telefono = cliente_json.get('telefono')
        email = cliente_json.get('email')
        return Cliente(id=id,
                       nombre=nombre,
                       apellido=apellido,
                       telefono=telefono,
                       email=email
                       )
