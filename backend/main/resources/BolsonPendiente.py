from flask_restful import Resource
from flask import request


BOLSONESPENDIENTES = {
    1: {'nombre:': 'Pendiente 1'},
    2: {'nombre:': 'Pendiente 2'},
}


class BolsonPendiente(Resource):
    def get(self, id):
        if int(id) in BOLSONESPENDIENTES:
            return BOLSONESPENDIENTES[int(id)]
        return '', 404

    def delete(self, id):
        if int(id) in BOLSONESPENDIENTES:
            del BOLSONESPENDIENTES[int(id)]
            return '', 204
        return '', 404

    def put(self, id):
        if int(id) in BOLSONESPENDIENTES:
            bolsonpendiente = BOLSONESPENDIENTES[int(id)]
            data = request.get_json()
            bolsonpendiente.update(data)
            return bolsonpendiente, 201
        return '', 204


class BolsonesPendientes(Resource):
    def get(self):
        return BOLSONESPENDIENTES

    def post(self):
        bolsonpendiente = request.get_json()
        id = int(max(BOLSONESPENDIENTES.keys())) + 1
        BOLSONESPENDIENTES[id] = bolsonpendiente
        return BOLSONESPENDIENTES[id], 201
