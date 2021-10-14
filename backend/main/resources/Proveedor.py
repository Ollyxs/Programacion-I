from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required, admin_provider_required


class Proveedor(Resource):
    # @admin_provider_required
    def get(self, id):
        proveedor = db.session.query(UsuarioModel).get_or_404(id)
        if proveedor.role == 'proveedor':
            return proveedor.to_json()
        else:
            return '', 404

    # @admin_required
    def delete(self, id):
        proveedor = db.session.query(UsuarioModel).get_or_404(id)
        if proveedor.role == 'proveedor':
            db.session.delete(proveedor)
            db.session.commit()
            return '', 204
        else:
            return '', 404

    # @admin_required
    def put(self, id):
        proveedor = db.session.query(UsuarioModel).get_or_404(id)
        if proveedor.role == 'proveedor':
            data = request.get_json().items()
            for key, value in data:
                setattr(proveedor, key, value)
            db.session.add(proveedor)
            db.session.commit()
            return proveedor.to_json(), 201
        else:
            return '', 404


class Proveedores(Resource):
    def get(self):
        page = 1
        per_page = 10
        proveedores = db.session.query(UsuarioModel).filter(UsuarioModel.role == 'proveedor')
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                if key == 'per_page':
                    per_page = int(value)
        proveedores = proveedores.paginate(page, per_page, True, 30)
        return jsonify({'proveedores': [proveedor.to_json() for proveedor in proveedores.items],
                'total': proveedores.total,
                'pages': proveedores.pages,
                'page': page
                })

    @admin_required
    def post(self):
        proveedor = UsuarioModel.from_json(request.get_json())
        if proveedor.role == 'proveedor':
            try:
                db.session.add(proveedor)
                db.session.commit()
            except Exception:
                return 'Formato no correcto', 400
            return proveedor.to_json(), 201
        else:
            return '', 404
