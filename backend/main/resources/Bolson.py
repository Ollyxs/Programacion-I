from flask_restful import Resource
from flask import request

BOLSONES = {
    1: {'nombre': 'Bolson 1'},
    2: {'nombre': 'Bolson 2'},
    3: {'nombre': 'Bolson 3'},
}


class Bolson(Resource):
    def get(self, id):
        if int(id) in BOLSONES:
            return BOLSONES[int(id)]
        return '', 404


class Bolsones(Resource):
    def get(self):
        return BOLSONES
