from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import BolsonModel


BOLSONESPREVIOS = {
    1: {'nombre': 'BolsonPrevio 1'},
    2: {'nombre': 'BolsonPrevio 2'},
}


class BolsonPrevio(Resource):
    def get(self, id):
        bolsonprevio = db.session.query(BolsonModel).get_or_404(id)
        return bolsonprevio.to_json()


class BolsonesPrevios(Resource):
    def get(self):
        bolsonesprevios = db.session.query(BolsonModel).all()
        return jsonify([bolsonprevio.to_json() for bolsonprevio in bolsonesprevios])
