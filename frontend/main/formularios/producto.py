from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask_wtf.file import FileField, FileRequired
from wtforms import validators


mess = "Campo obligatorio"


class FormProducto(FlaskForm):
    # imagen = FileField("",
    #         validators = [
    #             FileRequired(message="imagen obligatoria")
    #         ],
    #         )
    nombre = StringField("Nombre",
            [
                validators.Required(message=mess),
                validators.Length(max=100, message="El nombre debe tener menos de 100 caracteres")
            ],
                render_kw={"placeholder": "Nombre del producto"}
            )
    descripcion = StringField("Descripcion",
            [
                validators.Required(message=mess),
                validators.Length(max=500, message="La descripcion debe tener menos de 500 caracteres")
            ],
                render_kw={"placeholder": "Descripcion del producto"}
            )
    envio = SubmitField("Guardar cambios")


class FormFilterProducto(FlaskForm):
    proveedorid = SelectField('Proveedor', [validators.optional()], coerce = int,)
    envio = SubmitField("Filtrar")
