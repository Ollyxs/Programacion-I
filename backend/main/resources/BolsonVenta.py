from flask_restful import Resource
from flask import request


BOLSONESVENTAS = {
    1: {'nombre': 'BolsonVenta 1'},
    2: {'nombre': 'BolsonVenta 2'},
}


class BolsonVenta(Resource):
    def get(self, id):
        if int(id) in BOLSONESVENTAS:
            return BOLSONESVENTAS[int(id)]
        return '', 404


class BolsonesVentas(Resource):
    def get(self):
        return BOLSONESVENTAS
