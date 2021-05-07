from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required


class Proveedor(Resource):
    @jwt_required()
    def get(self, id):
        proveedor = db.session.query(UsuarioModel).get_or_404(id)
        if proveedor.role == 'proveedor':
            return proveedor.to_json()
        else:
            return '', 404

    @admin_required
    def delete(self, id):
        proveedor = db.session.query(UsuarioModel).get_or_404(id)
        if proveedor.role == 'proveedor':
            db.session.delete(proveedor)
            db.session.commit()
            return '', 204
        else:
            return '', 404

    @admin_required
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
    @jwt_required()
    def get(self):
        proveedores = db.session.query(UsuarioModel).filter(UsuarioModel.role == 'proveedor').all()
        return jsonify([proveedor.to_json() for proveedor in proveedores])

    @admin_required
    def post(self):
        proveedor = UsuarioModel.from_json(request.get_json())
        if proveedor.role == 'proveedor':
            try:
                db.session.add(proveedor)
                db.session.commit()
            except Exception as error:
                return 'Formato no correcto', 400
            return proveedor.to_json(), 201
        else:
            return '', 404
