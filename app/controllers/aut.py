from flask import Blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import db, Usuario

# CORREGIR RUTAS
aut = Blueprint('aut', __name__)

@aut.route('/registro', methods = ['GET', 'POST'])
def registro():
    if request.method == 'POST':
       nombre = request.form['nombre']
       correo = request.form['correo']
       contrasena = request.form['contrasena']
       usuario_check = Usuario.query.filter_by(correo = correo).first()
       if usuario_check:
        print('usuario ya esta registrado')

        contrasena_hash = generate_password_hash(contrasena)
        nuevo_usuario = Usuario(nombre = nombre, correo = correo, contrasena = contrasena_hash)
        db.session.add(nuevo_usuario)
        db.session.commit()
        login_user(nuevo_usuario)
        return redirect(url_for('nav.clientes'))

    return render_template('signup.html')

@aut.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        usuario = Usuario.query.filter_by(correo = correo).first()
        if usuario and check_password_hash(usuario.contrasena, contrasena):
            login_user(usuario)
            return redirect(url_for('nav.clientes'))
        else:
            print('error')
    return render_template('login.html')



@aut.route('/logout')
def logout():
    logout_user()  
    return redirect(url_for('login'))

    