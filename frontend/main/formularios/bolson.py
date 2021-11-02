from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, SubmitField, FloatField
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms.validators import InputRequired
from wtforms import validators


mess = "Campo obligatorio"


class FormBolson(FlaskForm):
    nombre = StringField("Nombre",
            [
                validators.Required(message=mess),
                validators.Length(max=100, message="El nombre debe tener menos de 100 caracteres")
            ],
                render_kw={"placeholder": "Nombre del bolsón"}
            )
    fecha = DateField("Fecha",
            [
                validators.Required()
            ],  format='%Y-%m-%d'
            )
    precio = FloatField("Precio $",
            [
                validators.Required(message=mess)
            ],
                render_kw={"placeholder": "99.99"}
            )
    productosId = SelectMultipleField("", coerce=int)
    envio = SubmitField("Crear bolsón")


class FormFilterBolson(FlaskForm):
    nombre = StringField('',[validators.optional()])
    desde = FloatField('', [validators.optional()])
    hasta = FloatField('',[validators.optional()])
    ordenamiento = SelectField('',
            choices=[('fecha', "Fecha"), ('asc',"Precio ascendente"), ('desc', "Precio descendente")],
            validators=[InputRequired()], coerce=str, default='fecha')
    envio = SubmitField("Filtrar")

class FormFilterBolsones(FlaskForm):
    desde = DateTimeField('',[validators.optional()], format='%Y-%m-%d')
    hasta = DateTimeField('',[validators.optional()], format='%Y-%m-%d')
    envio = SubmitField('Filtrar')
