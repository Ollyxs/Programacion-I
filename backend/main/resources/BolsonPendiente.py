from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import BolsonModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required, admin_provider_required


class BolsonPendiente(Resource):
    @admin_provider_required
    def get(self, id):
        bolsonpendiente = db.session.query(BolsonModel).get_or_404(id)
        if bolsonpendiente.aprobado == 0:
            return bolsonpendiente.to_json()
        else:
            return '', 404

    @admin_required
    def delete(self, id):
        bolsonpendiente = db.session.query(BolsonModel).get_or_404(id)
        db.session.delete(bolsonpendiente)
        db.session.commit()
        return '', 204

    @admin_required
    def put(self, id):
        bolsonpendiente = db.session.query(BolsonModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(bolsonpendiente, key, value)
        db.session.add(bolsonpendiente)
        db.session.commit()
        return bolsonpendiente.to_json(), 201


class BolsonesPendientes(Resource):
    @admin_provider_required
    def get(self):
        page = 1
        per_page = 10
        bolsonespendientes = db.session.query(BolsonModel).filter(BolsonModel.aprobado == 0)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page2':
                    page = int(value)
                if key == 'per_page2':
                    per_page = int(value)
        bolsonespendientes = bolsonespendientes.paginate(page, per_page, True, 30)
        return jsonify({'bolsones pendientes': [bolsonpendiente.to_json() for bolsonpendiente in bolsonespendientes.items],
                        'total': bolsonespendientes.total,
                        'pages2': bolsonespendientes.pages,
                        'page2': page
                        })

    @admin_required
    def post(self):
        try:
            bolsonpendiente = BolsonModel.from_json(request.get_json())
            print(bolsonpendiente)
            if isinstance (bolsonpendiente, str):
                print(bolsonpendiente)
                raise Exception(bolsonpendiente)
            else:
                db.session.add(bolsonpendiente)
                db.session.commit()
            print(123)
        except Exception as error:
            print(234)
            print(error)
            return str(error), 400
        print(345)
        return bolsonpendiente.to_json(), 201
