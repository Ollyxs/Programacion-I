from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import BolsonModel
import datetime


hoy = datetime.datetime.now()
fechaPrev = hoy - datetime.timedelta(weeks=1)


class BolsonVenta(Resource):
    def get(self, id):
        bolsonventa = db.session.query(BolsonModel).get_or_404(id)
        if bolsonventa.aprobado == 1:
            return bolsonventa.to_json()
        else:
            return '', 404


class BolsonesVentas(Resource):
    def get(self):
        page = 1
        per_page = 10
        bolsonesventas = db.session.query(BolsonModel).filter(BolsonModel.aprobado == 1, BolsonModel.fecha >= fechaPrev)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                if key == 'per_page':
                    per_page = int(value)
        bolsonesventas = bolsonesventas.paginate(page, per_page, True, 30)
        return jsonify({'bolsonesventas': [bolsonventa.to_json() for bolsonventa in bolsonesventas.items],
                        'total': bolsonesventas.total,
                        'pages': bolsonesventas.pages,
                        'page': page
                        })
