from flask import request, jsonify, Blueprint
from .. import db
from main.models import UsuarioModel
from main.auth.decorators import admin_required
from .functions import sendMail


mail = Blueprint('mail', __name__, url_prefix='/mail')


@mail.route('/promo', methods=['POST'])
#@admin_required
def promo():
    cliente = db.session.query(UsuarioModel).filter(UsuarioModel.role == 'cliente').all()
    lista_mails = [c.email for c in cliente]
    print(lista_mails)
    try:
        sent = sendMail([lista_mails], "Promocion!", 'promocion', cliente=cliente)
    except Exception as error:
        return str(error), 409
    return cliente.to_json(), 201
