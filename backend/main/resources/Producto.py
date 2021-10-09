from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoModel, UsuarioModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required, provider_required, admin_provider_required


class Producto(Resource):
    def get(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        return producto.to_json()

    # @admin_provider_required
    def delete(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        db.session.delete(producto)
        db.session.commit()
        return '', 204

    # @provider_required
    def put(self, id):
        proveedor = get_jwt_identity()
        producto = db.session.query(ProductoModel).get_or_404(id)
        if producto.proveedorid == proveedor:
            data = request.get_json().items()
            for key, value in data:
                setattr(producto, key, value)
            db.session.add(producto)
            db.session.commit()
            return producto.to_json(), 201
        else:
            return '', 404


class Productos(Resource):
    # @admin_provider_required
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

    # @provider_required
    def post(self):
        producto = ProductoModel.from_json(request.get_json())
        proveedor = get_jwt_identity()
        producto.proveedorid = proveedor
        try:
            db.session.add(producto)
            db.session.commit()
        except Exception:
            return 'Formato o ID no correcto', 400
        return producto.to_json(), 201
