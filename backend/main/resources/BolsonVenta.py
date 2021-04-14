from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import BolsonModel


BOLSONESVENTAS = {
    1: {'nombre': 'BolsonVenta 1'},
    2: {'nombre': 'BolsonVenta 2'},
}


class BolsonVenta(Resource):
    def get(self, id):
        bolsonventa = db.session.query(BolsonModel).get_or_404(id)
        return bolsonventa.to_json()


class BolsonesVentas(Resource):
    def get(self):
        bolsonesventas = db.session.query(BolsonModel).all()
        return jsonify([bolsonventa.to_json() for bolsonventa in bolsonesventas])
