from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import BolsonModel
import datetime
from main.auth.decorators import admin_required


hoy = datetime.datetime.now()
fechaPrev = hoy - datetime.timedelta(weeks=1)


class BolsonPrevio(Resource):
    @admin_required
    def get(self, id):
        bolsonprevio = db.session.query(BolsonModel).get_or_404(id)
        if bolsonprevio.fecha <= fechaPrev:
            return bolsonprevio.to_json()
        else:
            return '', 404


class BolsonesPrevios(Resource):
    @admin_required
    def get(self):
        page = 1
        per_page = 10
        bolsonesprevios = db.session.query(BolsonModel).filter(BolsonModel.fecha <= fechaPrev)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                if key == 'per_page':
                    per_page = int(value)
        bolsonesprevios = bolsonesprevios.paginate(page, per_page, True, 30)
        return jsonify({'bolsones previos': [bolsonprevio.to_json() for bolsonprevio in bolsonesprevios.items],
                        'total': bolsonesprevios.total,
                        'pages': bolsonesprevios.pages,
                        'page': page
                        })
