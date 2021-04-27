from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CompraModel, ClienteModel, BolsonModel


class Compra(Resource):
    def get(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        return compra.to_json()

    def delete(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        db.session.delete(compra)
        db.session.commit()
        return '', 204

    def put(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(compra, key, value)
        db.session.add(compra)
        db.session.commit()
        return compra.to_json(), 201


class Compras(Resource):
    def get(self):
        page = 1
        per_page = 10
        compras = db.session.query(CompraModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
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

    def post(self):
        compra = CompraModel.from_json(request.get_json())
        cliente = db.session.query(ClienteModel).get_or_404(compra.clienteid)
        bolson = db.session.query(BolsonModel).get_or_404(compra.bolsonid)
        try:
            db.session.add(compra)
            db.session.commit()
        except:
            return 'Formato no correcto', 400
        return compra.to_json(), 201
