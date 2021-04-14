from flask_restful import Resource
from flask import request
from .. import db
from main.models import BolsonModel

BOLSONES = {
    1: {'nombre': 'Bolson 1'},
    2: {'nombre': 'Bolson 2'},
    3: {'nombre': 'Bolson 3'},
}


class Bolson(Resource):
    def get(self, id):
        bolson = db.session.query(BolsonModel).get_or_404(id)
        return bolson.to_json()


class Bolsones(Resource):
    def get(self):
        bolsones = db.session.query(BolsonModel).all()
        return jsonify([bolson.to_json() for bolson in bolsones])
