from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import BolsonModel
import datetime


hoy = datetime.datetime.now()
fechaPrev = hoy - datetime.timedelta(weeks=1)


class BolsonPrevio(Resource):
    def get(self, id):
        bolsonprevio = db.session.query(BolsonModel).get_or_404(id)
        return bolsonprevio.to_json()


class BolsonesPrevios(Resource):
    def get(self):
        bolsonesprevios = db.session.query(BolsonModel).filter(BolsonModel.fecha <= fechaPrev).all()
        return jsonify([bolsonprevio.to_json() for bolsonprevio in bolsonesprevios])
