from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField


class FormCompra(FlaskForm):
    bolsonId = IntegerField(label=None)
    envio = SubmitField("Comprar")
