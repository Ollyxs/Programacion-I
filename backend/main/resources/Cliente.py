from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required, client_required, admin_client_required


class Cliente(Resource):
    @admin_client_required
    def get(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        iduser = get_jwt_identity()
        user = db.session.query(UsuarioModel).get_or_404(iduser)
        if user.role == 'admin' and cliente.id != iduser and cliente.role == 'cliente':
            return cliente.to_json()
        elif user.role == 'cliente' and cliente.id == iduser:
            return cliente.to_json()
        else:
            return '', 404

    @admin_client_required
    def delete(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        iduser = get_jwt_identity()
        user = db.session.query(UsuarioModel).get_or_404(iduser)
        if user.role == 'admin' and cliente.id != iduser and cliente.role == 'cliente':
            db.session.delete(cliente)
            db.session.commit()
            return '', 204
        elif user.role == 'cliente' and cliente.id == iduser:
            db.session.delete(cliente)
            db.session.commit()
            return '', 204
        else:
            return '', 404

    @client_required
    def put(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        clienteid = get_jwt_identity()
        if cliente.id == clienteid:
            if cliente.validate_pass(request.get_json().get("contra")):
                data = request.get_json().items()
                for key, value in data:
                    setattr(cliente, key, value)
                db.session.add(cliente)
                db.session.commit()
                return cliente.to_json(), 201
            else:
                return 'Incorrect password', 401
        else:
            return '', 404


class Clientes(Resource):
    @admin_required
    def get(self):
        page = 1
        per_page = 10
        clientes = db.session.query(UsuarioModel).filter(UsuarioModel.role == 'cliente')
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'ordenamiento':
                    if value == 'nombre':
                        clientes = clientes.order_by(UsuarioModel.nombre.asc())
                    if value == 'apellido':
                        clientes = clientes.order_by(UsuarioModel.apellido.asc())
                if key == 'page':
                    page = int(value)
                if key == 'per_page':
                    per_page = int(value)
        clientes = clientes.paginate(page, per_page, True, 30)
        return jsonify({'clientes': [cliente.to_json() for cliente in clientes.items],
                        'total': clientes.total,
                        'pages': clientes.pages,
                        'page': page
                        })

    def post(self):
        cliente = UsuarioModel.from_json(request.get_json())
        emailcheck = db.session.query(UsuarioModel).filter(UsuarioModel.email == cliente.email)
        if emailcheck:
            try:
                db.session.add(cliente)
                db.session.commit()
            except Exception:
                return 'Formato no correcto', 400
            return cliente.to_json(), 201
        else:
            return 'Email alredy in use', 409
