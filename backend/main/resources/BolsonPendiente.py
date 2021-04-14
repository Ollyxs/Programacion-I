from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import BolsonModel

BOLSONESPENDIENTES = {
    1: {'nombre:': 'Pendiente 1'},
    2: {'nombre:': 'Pendiente 2'},
}


class BolsonPendiente(Resource):
    def get(self, id):
        bolsonpendiente = db.session.query(BolsonModel).get_or_404(id)
        return bolsonpendiente.to_json()

    def delete(self, id):
        bolsonpendiente = db.session.query(BolsonModel).get_or_404(id)
        db.session.delete(bolsonpendiente)
        db.session.commit()
        return '', 204

    def put(self, id):
        bolsonpendiente = db.session.query(BolsonModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(bolsonpendiente, key, value)
        db.session.add(bolsonpendiente)
        db.session.commit()
        return bolsonpendiente.to_json(), 201


class BolsonesPendientes(Resource):
    def get(self):
        bolsonespendientes = db.session.query(BolsonModel).all()
        return jsonify([bolsonpendiente.to_json() for bolsonpendiente in bolsonespendientes])

    def post(self):
        bolsonpendiente = BolsonModel.from_json(request.get_json())
        db.session.add(bolsonpendiente)
        db.session.commit()
        return bolsonpendiente.to_json(), 201
