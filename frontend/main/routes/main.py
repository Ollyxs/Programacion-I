from flask import Blueprint, url_for, render_template

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def index():
    return render_template('index.html')
