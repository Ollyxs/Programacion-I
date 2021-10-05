from flask import Blueprint, render_template, redirect, url_for
from .. formularios.registrarse import FormRegistro
from .. formularios.ingresar import FormIngreso
from .. formularios.cuenta import FormCuenta


usuarios = Blueprint('usuarios', __name__, url_prefix='/usuarios')

USUARIOS = [
        {"id":0,"nombre":"Lucas","apellido":"Ollarce","telefono":"2604000000","email":"l.ollarce@mail.com","password":"12345","role":"admin"},
        {"id":1,"nombre":"Juan","apellido":"Perez","telefono":"2604000000","email":"j.perez@mail.com","password":"12345","role":"proveedor"},
        {"id":2,"nombre":"Martín","apellido":"Lopez","telefono":"2604000000","email":"m.martin@mail.com","password":"12345","role":"proveedor"},
        {"id":3,"nombre":"Marta","apellido":"Contreras","telefono":"2604000000","email":"m.contreras@mail.com","password":"12345","role":"proveedor"},
        {"id":4,"nombre":"Oscar","apellido":"Gonzalez","telefono":"2604000000","email":"o.gonzalez@mail.com","password":"12345","role":"proveedor"},
        {"id":5,"nombre":"Ana","apellido":"Barrera","telefono":"2604000000","email":"a.barrera@mail.com","password":"12345","role":"proveedor"},
        {"id":6,"nombre":"Karen","apellido":"García","telefono":"2604000000","email":"k.garcia@mail.com","password":"12345","role":"proveedor"},
        {"id":7,"nombre":"Carlos","apellido":"Moreno","telefono":"2604000000","email":"c.moreno@mail.com","password":"12345","role":"proveedor"},
        {"id":8,"nombre":"Jesus","apellido":"Mitre","telefono":"2604000000","email":"j.mitre@mail.com","password":"12345","role":"cliente"},
        {"id":9,"nombre":"Jorge","apellido":"Perez","telefono":"2604000000","email":"jo.perez@mail.com","password":"12345","role":"cliente"},
        {"id":10,"nombre":"María","apellido":"Silva","telefono":"2604000000","email":"m.silva@mail.com","password":"12345","role":"cliente"},
        ]

@usuarios.route('/registrar', methods=['POST', 'GET'])
def registrar():
    form = FormRegistro()
    if form.validate_on_submit():
        print(form.nombre.data)
        return redirect(url_for('main.index'))
    return render_template('registrarse.html', formulario=form)

@usuarios.route('/ingresar', methods=['POST', 'GET'])
def ingresar():
    form = FormIngreso()
    if form.validate_on_submit():
        print(form.email.data)
        return redirect(url_for('main.index'))
    return render_template('ingresar.html', formulario=form)

@usuarios.route('mi-cuenta/<int:id>')
def mi_cuenta(id):
    return render_template('usuario.html', usuario = USUARIOS[id])

@usuarios.route('admin', methods=['POST', 'GET'])
def admin():
    form = FormCuenta()
    if form.validate_on_submit():
        print(form.name.data)
        return redirect(url_for('usuario.admin'))
    return render_template('admin.html', formulario=form)
