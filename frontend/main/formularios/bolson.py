from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField
from wtforms.fields.html5 import DateField
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
    productosId = SelectMultipleField("", coerce=int)
    envio = SubmitField("Crear bolsón")


class FormFilterBolson(FlaskForm):
    nombre = StringField('',[validators.optional()])
    envio = SubmitField("Filtrar")
