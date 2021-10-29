from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CompraModel, BolsonModel, UsuarioModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required, client_required, admin_client_required


class Compra(Resource):
    @admin_client_required
    def get(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        return compra.to_json()

    @admin_required
    def delete(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        db.session.delete(compra)
        db.session.commit()
        return '', 204

    @admin_required
    def put(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(compra, key, value)
        db.session.add(compra)
        db.session.commit()
        return compra.to_json(), 201


class Compras(Resource):
    @admin_client_required
    def get(self):
        page = 1
        per_page = 10
        iduser = get_jwt_identity()
        user = db.session.query(UsuarioModel).get_or_404(iduser)
        if user.role == 'admin':
            compras = db.session.query(CompraModel)
        if user.role == 'cliente':
            compras = db.session.query(CompraModel).filter(CompraModel.clienteid == iduser).order_by(CompraModel.fechaHoraCompra.desc())
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'nombre':
                    compras = compras.join(UsuarioModel, CompraModel.cliente).filter(UsuarioModel.nombre.like('%'+value+'%'))
                if key == 'apellido':
                    compras = compras.join(UsuarioModel, CompraModel.cliente).filter(UsuarioModel.apellido.like('%'+value+'%'))
                if key == 'retirado':
                    if value != 2:
                        compras = compras.filter(CompraModel.retirado == value)
                if key == 'ordenamiento':
                    if value == 'id':
                        compras = compras.order_by(CompraModel.id.desc())
                    if value == 'fecha':
                        compras = compras.order_by(CompraModel.fechaHoraCompra.asc())
                    if value == 'nombre':
                        compras = compras.join(UsuarioModel, CompraModel.cliente).order_by(UsuarioModel.nombre.asc())
                    if value == 'apellido':
                        compras = compras.join(UsuarioModel, CompraModel.cliente).order_by(UsuarioModel.apellido.asc())
                if key == 'page':
                    page = int(value)
                if key == 'per_page':
                    per_page = int(value)
        compras = compras.paginate(page, per_page, True, 30)
        return jsonify({'compras': [compra.to_json() for compra in compras.items],
                        'total': compras.total,
                        'pages': compras.pages,
                        'page': page
                        })

    @client_required
    def post(self):
        compra = CompraModel.from_json(request.get_json())
        bolson = db.session.query(BolsonModel).get_or_404(compra.bolsonid)
        cliente = get_jwt_identity()
        compra.clienteid = cliente
        if bolson.aprobado == 1:
            try:
                db.session.add(compra)
                db.session.commit()
            except Exception:
                return 'Formato no correcto', 400
            return compra.to_json(), 201
        else:
            return 'ID de bolson no correcto', 400
