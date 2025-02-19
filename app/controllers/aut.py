from flask import Blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import db, Usuario


aut = Blueprint('aut', __name__)

# Registro de usuario
@aut.route('/registro', methods = ['GET','POST'])
def registro():
    if request.method == 'POST':
        try:
            # Recibir datos del formulario
            nombre = request.form['nombre']
            correo = request.form['correo']
            contrasena = request.form['contrasena']
            # Verificar espacios en blanco
            if nombre == '' or correo == '' or contrasena == '':
                flash('Datos inválidos.', 'error')
                return redirect(url_for('aut.registro'))
            # Verificar si el usuario ya existe
            usuario_check = Usuario.query.filter_by(correo = correo).first()
            if usuario_check:
                flash('El usuario ya existe.', 'error')
                return redirect(url_for('aut.registro'))
            # Registrar usuario
            contrasena_hash = generate_password_hash(contrasena)
            nuevo_usuario = Usuario(nombre = nombre, correo = correo, contrasena = contrasena_hash)
            db.session.add(nuevo_usuario)
            db.session.commit()
            login_user(nuevo_usuario)
            flash('El usuario se ha registrado.', 'success')
            return redirect(url_for('nav.clientes'))

        except Exception as e:
            print(e)

    return render_template('signup.html')

# Inicio se sesión
@aut.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            # Recibir datos del formulario
            correo = request.form['correo']
            contrasena = request.form['contrasena']
            # Verificar espacios en blanco
            if correo == '' or contrasena == '':
                flash('Correo o contraseña invalidos.', 'error')
                return redirect(url_for('aut.login'))
            # Verificar si el usuario existe
            correo_check = Usuario.query.filter_by(correo = correo).first()
            if correo_check and check_password_hash(correo_check.contrasena, contrasena):
                # Logear usuario
                flash('Bienvenido ' + correo_check.nombre, 'success')
                login_user(correo_check)
                return redirect(url_for('nav.clientes'))
            else:
                flash('Correo o contraseña incorrecta', 'error')
                return redirect(url_for('aut.login'))

        except Exception as e:
            print(e)

    return render_template('login.html')

# Cerrar sesión
@aut.route('/logout')
def logout():
    # Cerrar la sesión del usuario y mostrar notificación
    logout_user() 
    flash('Sesión terminada', 'success')
    return redirect(url_for('aut.login'))

    