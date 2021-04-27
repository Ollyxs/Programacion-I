from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoModel, ProveedorModel


class Producto(Resource):
    def get(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        return producto.to_json()

    def delete(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        db.session.delete(producto)
        db.session.commit()
        return '', 204

    def put(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(producto, key, value)
        db.session.add(producto)
        db.session.commit()
        return producto.to_json(), 201


class Productos(Resource):
    def get(self):
        page = 1
        per_page = 10
        productos = db.session.query(ProductoModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                if key == 'per_page':
                    per_page = int(value)
        productos = productos.paginate(page, per_page, True, 30)
        return jsonify({'productos': [producto.to_json() for producto in productos.items],
                        'total': productos.total,
                        'pages': productos.pages,
                        'page': page
                        })

    def post(self):
        producto = ProductoModel.from_json(request.get_json())
        proveedor = db.session.query(ProveedorModel).get_or_404(producto.proveedorid)
        try:
            db.session.add(producto)
            db.session.commit()
        except:
            return 'Formato no correcto', 400
        return producto.to_json(), 201
