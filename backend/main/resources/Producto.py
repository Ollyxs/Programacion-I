from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoModel, UsuarioModel, BolsonModel, BolsonProductoModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required, provider_required, admin_provider_required
import datetime


hoy = datetime.datetime.now()
fechaPrev = hoy - datetime.timedelta(weeks=1)

class Producto(Resource):
    def get(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        return producto.to_json()

    @admin_provider_required
    def delete(self, id):
        iduser = get_jwt_identity()
        producto = db.session.query(ProductoModel).get_or_404(id)
        print(producto)
        print(producto.id)
        bolsonesventas = db.session.query(BolsonModel).filter(BolsonModel.aprobado == 1, BolsonModel.fecha >= fechaPrev).filter(BolsonModel.productos).join(BolsonProductoModel,
                    BolsonModel.productos).join(ProductoModel,
                    BolsonProductoModel.producto).filter(ProductoModel.id == producto.id)
        productos_bolson = []
        for a in bolsonesventas:
            print(a)
            print(a.productos)
            for i in a.productos:
                print(i)
                print(i.productoid)
                productos_bolson.append(i.productoid)
        if producto.id not in productos_bolson:
            db.session.delete(producto)
            db.session.commit()
            return '', 204
        else:
            return 'El producto no se puede eliminar mientra pertenezca a un bolson en venta.', 405

    @provider_required
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
    @admin_provider_required
    def get(self):
        page = 1
        per_page = 10
        iduser = get_jwt_identity()
        user = db.session.query(UsuarioModel).get_or_404(iduser)
        if user.role == 'admin':
            productos = db.session.query(ProductoModel)
        if user.role == 'proveedor':
            productos = db.session.query(ProductoModel).filter(ProductoModel.proveedorid == iduser)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'proveedorid':
                    productos = productos.filter(ProductoModel.proveedorid == value)
                if key == 'ordenamiento':
                    if value == 'producto':
                        productos = productos.order_by(ProductoModel.nombre.asc())
                    if value == 'proveedor':
                        productos = productos.join(UsuarioModel, ProductoModel.proveedor).order_by(UsuarioModel.nombre.asc())
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

    @provider_required
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
