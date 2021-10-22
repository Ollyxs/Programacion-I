from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField, SelectField
from wtforms.validators import InputRequired
from wtforms import validators


class FormCompra(FlaskForm):
    bolsonId = IntegerField(label=None)
    envio = SubmitField("Comprar")


class FormFilterCompra(FlaskForm):
    nombre = StringField('',[validators.optional()])
    apellido = StringField('',[validators.optional()])
    retirado = SelectField('', [validators.optional()], choices = [(2, ""), (1, "Si"), (0, "No")], coerce = int, default=2)
    ordenamiento = SelectField('',
            choices = [('id', "N° Compra"), ('fecha', "Fecha Compra"), ('nombre', "Nombre Cliente"), ('apellido', "Apellido Cliente")],
            validators=[InputRequired()], coerce=str, default='id')
    envio = SubmitField("Filtar/Ordenar")
