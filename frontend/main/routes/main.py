from flask import Blueprint, url_for, render_template, current_app, redirect
# from . import bolsones
import requests, json

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def index():
    data = {}
    data['page'] = 1
    r = requests.get(
            current_app.config['API_URL']+'/bolsones-venta',
            headers ={"content-type": "application/json"},
            data = json.dumps(data))
    bolsones = json.loads(r.text)["bolsonesventas"]
    return render_template('index.html', bolsones = bolsones)
