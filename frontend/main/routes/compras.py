from flask import Blueprint, render_template, redirect, url_for, current_app, request
from flask_login import login_required, LoginManager, current_user
import requests, json
from .auth import admin_required, cliente_required


compras = Blueprint('compras', __name__, url_prefix='/compras')


@compras.route('/ver/<int:id>')
@login_required
@admin_required
def ver(id):
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}
    r = requests.get(
            current_app.config['API_URL']+'/compra/'+str(id),
            headers = headers)
    if (r.status_code == 404):
        return redirect(url_for('compras.ver_todas'))
    compra = json.loads(r.text)
    print(compra)
    return render_template('ver_modificar_compra.html', compra = compra)

@compras.route('/todas')
@login_required
@admin_required
def ver_todas():
    data = {}
    data['page'] = 1
    data['per_page'] = 10
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}
    r = requests.get(
            current_app.config['API_URL']+'/compras',
            headers = headers,
            data = json.dumps(data))
    compras = json.loads(r.text)["compras"]
    return render_template('compras_admin.html', compras = compras)
