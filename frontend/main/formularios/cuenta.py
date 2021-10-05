from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField, TelField
from wtforms import validators


mess = "Campo obligatorio"


class FormCuenta(FlaskForm):
    nombre = StringField("Nombre",
        [
            validators.Required(message=mess),
            validators.Length(max=100, message="El nombre debe tener menos de 100 caracteres")
        ],
            render_kw={"value": "Lucas"}
        )
    apellido = StringField("Apellido",
        [
            validators.Required(message=mess),
            validators.Length(max=100, message="Apellido debe tener menos de 100 caracteres")
        ],
            render_kw={"value": "Ollarce"}
        )
    email = EmailField("Email",
        [
            validators.Required(message=mess),
            validators.Email(message="Formato incorrecto"),
            validators.Length(max=100, message="El email debe tener menos de 100 caracteres")
        ],
            render_kw={"value": "l.ollarce@example.com"}
        )
    telefono = TelField("Telefono",
        [
            validators.Required(message=mess),
            validators.Length(max=100, min=10, message="El email debe tener entre 10 y 100 caracteres")
        ],
            render_kw={"value": "2604000000"}
        )
    password = PasswordField("Contraseña",
        [
            validators.Required(message=mess),
            validators.EqualTo("confirmar", message="Las contraseñas no coinciden"),
            validators.Length(max=128, min=8, message="La contraseña debe tener entre 8 y 128 caracteres")
        ],
            render_kw={"value": "**********"}
        )
    confirmar = PasswordField("Confirmar contraseña", render_kw={"value": "**********"})
    envio = SubmitField("Guardar cambios")
