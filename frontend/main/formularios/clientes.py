from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import InputRequired
from wtforms import validators


class FormFilterCliente(FlaskForm):
    ordenamiento = SelectField('',
            choices=[('nombre',"Nombre"),('apellido',"Apellido")],
            validators=[InputRequired()], coerce=str, default='nombre')
    envio = SubmitField("ordenar")
