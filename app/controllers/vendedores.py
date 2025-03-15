from flask import Blueprint, render_template, request, redirect, url_for, json, flash, jsonify
from app.models.models import db, Vendedor
from flask_login import login_required
vendedor = Blueprint('vendedor', __name__)

# Registrar vendedor
@vendedor.route('/registrar_vendedor', methods = ['POST'])
@login_required
def registrar_vendedor():
    try:
        # Datos del formulario
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        # Validación
        if not (nombre and correo and telefono and direccion):
            flash('Datos inválidos.', 'error')
            return redirect (url_for('nav.vendedores'))
        # Verificar si existe el vendedor
        correo_verificacion = Vendedor.query.filter_by(correo = correo).first()
        if correo_verificacion:
            flash('El correo ingresado ya se encuentra registrado', 'error')
            return redirect(url_for('nav.vendedores'))
        # Registrar vendedor
        vendedor = Vendedor(nombre = nombre, correo = correo, telefono = telefono, direccion = direccion)
        db.session.add(vendedor)
        db.session.commit()
        flash('El vendedor se ha registrado', 'success')
        return redirect(url_for('nav.vendedores'))
    except Exception as e:
        db.session.rollback()
        print(e)
        flash('Hubo un error', 'error')
    return render_template('vendedores.html')

# Obtener información de un vendedor
@vendedor.route('/get_vendedor')
@login_required
def get_vendedor():
    id = request.args.get('id')
    vendedor = Vendedor.query.filter_by(id = id).first()
    if vendedor:
        return jsonify(vendedor.to_dict()), 200
    else:
        return jsonify({'mensaje' : 'Cliente no encontrado.'})

# Actualizar datos vendedor
@vendedor.route('/actualizar_vendedor', methods = ['POST'])
@login_required
def actualizar_vendedor():
    try:
        id = request.form.get('id_readonly')
        nombre = request.form.get('info_nombre')
        correo = request.form.get('info_correo')
        telefono = request.form.get('info_telefono')
        direccion = request.form.get('info_direccion')
        # Validación
        if not (id and nombre and correo and telefono and direccion):
            flash('Datos inválidos.', 'error')
            return redirect(url_for('nav.vendedores'))
        # Buscar vendedor en la base de datos
        vendedor = Vendedor.query.filter_by(id = id).first()
        if vendedor:
            # Actualizar datos
            vendedor.nombre = nombre
            vendedor.correo = correo
            vendedor.telefono = telefono
            vendedor.direccion = direccion
            db.session.commit()
            flash('Se han actualizado los datos del vendedor.', 'success')
            return redirect(url_for('nav.vendedores'))
    except Exception as e:
        print(e)
        flash('Hubo un error.', 'error')
        return redirect(url_for('nav.vendedores'))

# Eliminar vendedor
@vendedor.route('/eliminar_vendedor', methods = ['POST'])
@login_required
def eliminar_vendedor():
    try:
        id_vendedor = request.form.get('id')
        # Validación
        if not id_vendedor:
            flash('Hubo un error. El vendedor no se ha registrado.', 'error')
            return redirect(url_for('nav.vendedores'))
        # Buscar vendedor en BD
        vendedor = Vendedor.query.filter_by(id = id_vendedor).first()
        if vendedor:
            # Eliminar cliente
            db.session.delete(vendedor)
            db.session.commit()
            flash('El vendedor ha sido eliminado.', 'success')
            return redirect(url_for('nav.vendedores'))
        else:
            flash('Vendedor no encontrado.', 'error')
            return redirect(url_for('nav.vendedores'))
    except Exception as e:
        print(e)
        flash('Hubo un error.', 'error')
        return redirect(url_for('nav.vendedores'))