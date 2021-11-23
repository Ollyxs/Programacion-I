from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from main.auth.decorators import admin_required, client_required, admin_client_required


class Admin(Resource):
    @admin_required
    def get(self, id):
        admin = db.session.query(UsuarioModel).get_or_404(id)
        adminid = get_jwt_identity()
        if admin.id == adminid and admin.role == 'admin':
            return admin.to_json()
        else:
            return '', 404

    @admin_required
    def delete(self, id):
        admin = db.session.query(UsuarioModel).get_or_404(id)
        iduser = get_jwt_identity()
        user = db.session.query(UsuarioModel).get_or_404(iduser)
        if user.role == 'admin' and admin.id != iduser and admin.role == 'admin':
            db.session.delete(admin)
            db.session.commit()
            return '', 204
        elif user.role == 'admin' and admin.id == iduser:
            db.session.delete(admin)
            db.session.commit()
            return '', 204
        else:
            return '', 404

    @admin_required
    def put(self, id):
        admin = db.session.query(UsuarioModel).get_or_404(id)
        adminid = get_jwt_identity()
        if admin.id == adminid:
            if admin.validate_pass(request.get_json().get("contra")):
                data = request.get_json().items()
                for key, value in data:
                    setattr(admin, key, value)
                db.session.add(admin)
                db.session.commit()
                return admin.to_json(), 201
            else:
                return 'Incorrect password', 401
        else:
            return '', 404
