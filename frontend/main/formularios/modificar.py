from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import InputRequired
from wtforms import validators


class FormModificar(FlaskForm):
    aprobado = SelectField("Aprobado: ",
            choices=[(True, 'Si'),(False, 'No')],
            validators=[InputRequired()],
            coerce=lambda x: x == 'True')
    envio = SubmitField("Guardar cambios")
