from flask import Blueprint, render_template, request, redirect, url_for, json, flash, jsonify
from app.models.models import db, Vendedor
vendedor = Blueprint('vendedor', __name__)

# Registrar vendedor
@vendedor.route('/registrar_vendedor', methods = ['POST'])
def registrar_vendedor():
    nombre = request.form['nombre']
    correo = request.form['correo']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    try:
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

# Get datos vendedor
@vendedor.route('/get_vendedor')
def get_vendedor():
    id = request.args.get('id')
    vendedor = Vendedor.query.filter_by(id = id).first()
    if vendedor:
        return jsonify(vendedor.to_dict())
    else:
        print('El vendedor no existe')

# Actualizar datos vendedor
@vendedor.route('/actualizar_vendedor', methods = ['POST'])
def actualizar_vendedor():
    id = request.form.get('id_readonly')
    nombre = request.form.get('info_nombre')
    correo = request.form.get('info_correo')
    telefono = request.form.get('info_telefono')
    direccion = request.form.get('info_direccion')
    vendedor = Vendedor.query.filter_by(id = id).first()
    if vendedor:
        try:
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
def eliminar_vendedor():
    id_vendedor = request.form['id']
    try:
        vendedor = Vendedor.query.filter_by(id = id_vendedor).first()
        db.session.delete(vendedor)
        db.session.commit()
        flash('El vendedor ha sido eliminado.', 'success')
        return redirect(url_for('nav.vendedores'))
    except Exception as e:
        print(e)
        flash('Hubo un error.', 'error')
        return redirect(url_for('nav.vendedores'))