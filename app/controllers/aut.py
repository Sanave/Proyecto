from flask import Blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import db, Usuario


aut = Blueprint('aut', __name__)

# Registro de usuario
@aut.route('/registro', methods = ['GET','POST'])
def registro():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            correo = request.form['correo']
            contrasena = request.form['contrasena']

            usuario_check = Usuario.query.filter_by(correo = correo).first()
            if usuario_check:
                print('El usuario ya existe.')
                return redirect(url_for('aut.registro'))
            
            contrasena_hash = generate_password_hash(contrasena)
            nuevo_usuario = Usuario(nombre = nombre, correo = correo, contrasena = contrasena_hash)
            db.session.add(nuevo_usuario)
            db.session.commit()
            login_user(nuevo_usuario)
            print('El usuario ha sido registrado.')
            return redirect(url_for('nav.clientes'))

        except Exception as e:
            print(e)

    return render_template('signup.html')

# Inicio se sesión
@aut.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            correo = request.form['correo']
            contrasena = request.form['contrasena']

            correo_check = Usuario.query.filter_by(correo = correo).first()
            if correo_check and check_password_hash(correo_check.contrasena, contrasena):
                print('Usuario logeado.')
                login_user(correo_check)
                return redirect(url_for('nav.clientes'))
            else:
                print('datos incorrectos')
                return redirect(url_for('aut.login'))

        except Exception as e:
            print(e)

    return render_template('login.html')

# Cerrar sesión
@aut.route('/logout')
def logout():
    logout_user() 
    print('Sesión cerrada') 
    return redirect(url_for('aut.login'))

    