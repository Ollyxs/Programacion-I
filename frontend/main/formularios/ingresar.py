from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms import validators

mess = "Campo obligatorio"


class FormIngreso(FlaskForm):
    email = EmailField("Email",
        [
            validators.Required(message=mess),
            validators.Email(message="Formato incorrecto"),
            validators.Length(max=100)
        ]
    )
    password = PasswordField("Contraseña",
        [
            validators.Required(message=mess),
            validators.Length(max=128, min=8, message="La contraseña debe tener entre 8 y 128 caracteres")
        ]
        )
    envio = SubmitField("Ingresar")
