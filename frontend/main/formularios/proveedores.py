from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import InputRequired
from wtforms import validators


class FormFilterProveedor(FlaskForm):
    ordenamiento = SelectField('',
            choices=[('nombre', "nombre"), ('apellido', "apellido")],
            validators=[InputRequired()], coerce=str)
    envio = SubmitField("ordenar")
