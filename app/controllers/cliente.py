from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models.models import db, Cliente, Compra, Factura
cliente = Blueprint('cliente', __name__)

# Registrar clientes
@cliente.route('/registrar_cliente', methods = ['POST'])
def registrar_cliente():
    if request.method == 'POST':
        try:
            # Datos del formulario
            nombre = request.form.get('nombre')
            correo = request.form.get('correo')
            telefono = request.form.get('telefono')
            direccion = request.form.get('direccion')
            tipo_cliente = request.form.get('tcliente')
            # Validación
            if not (nombre and correo and telefono and direccion and tipo_cliente):
                flash('Datos no validos', 'error')
                return redirect(url_for('nav.clientes'))
            # Verificar correo
            correo = Cliente.query.filter_by(correo = correo)
            if correo:
                flash('El correo ingresado ya se encuentra registrado', 'error')
                return redirect(url_for('nav.clientes'))
            # Registrar cliente
            cliente = Cliente(nombre = nombre, correo = correo, telefono = telefono, direccion = direccion, tipo_cliente = tipo_cliente, estado = 'activo')
            db.session.add(cliente)
            db.session.commit()
            flash('El cliente se ha registrado.', 'success')
            return redirect(url_for('nav.clientes'))
        except Exception as e:
            db.session.rollback()
            print(e)
            flash('Hubo un error. No se ha registrado el cliente.', 'error')
    return render_template('clientes.html')


# Eliminar clientes
@cliente.route('/eliminar_cliente', methods=['POST'])
def eliminar_cliente():
    try:
        cliente_id = request.form.get('id')
        # Validación
        if not cliente_id:
            flash('Hubo un error. El cliente no se ha eliminado.', 'error')
            return redirect(url_for('nav.clientes'))
        # Buscar cliente en BD
        cliente = Cliente.query.filter_by(id = cliente_id).first()
        if cliente:
            # Eliminar el cliente
            db.session.delete(cliente)
            db.session.commit()
            flash('El cliente se ha eliminado', 'success')
            return redirect(url_for('nav.clientes'))
        else:
            flash('Cliente no encontrado.', 'error')
            return redirect(url_for('nav.clientes'))
    except Exception as e:
        db.session.rollback() 
        print(e)
        flash('Hubo un error.')
        return redirect(url_for('nav.clientes'))
    return render_template('clientes.html')


# Obtener información de un cliente
@cliente.route('/get_cliente')
def get_cliente():
    id = request.args.get('id')
    cliente = Cliente.query.filter_by(id = id).first()
    if cliente:
        return jsonify(cliente.to_dict()), 200
    else:
        return jsonify({'mensaje' : 'Cliente no encontrado'}), 404


# Actualizar información de un cliente
@cliente.route('/actualizar_cliente', methods = ['POST'])
def actualizar_cliente():
    try:
    # Datos del formulario
        id = request.form.get('id_readonly')
        nombre = request.form.get('info_nombre')
        correo = request.form.get('info_correo')
        telefono = request.form.get('info_telefono')
        direccion = request.form.get('info_direccion')
        tcliente = request.form.get('info_tcliente')
        # Validación
        if not (id and nombre and correo and telefono and direccion and tcliente):
            flash('Datos inválidos.', 'error')
            return redirect(url_for('nav.clientes'))
        # Buscar cliente en la base de datos
        cliente = Cliente.query.filter_by(id = id).first()
        if cliente:
                # Actualizar datos
                cliente.nombre = nombre
                cliente.correo = correo
                cliente.telefono = telefono
                cliente.direccion = direccion
                cliente.tipo_cliente = tcliente
                db.session.commit()
                flash('Se han actualizado los datos del cliente.', 'success')
                return redirect(url_for('nav.clientes'))
        else:
            flash('Cliente no encontrado.', 'error')
            return redirect(url_for('nav.clientes'))

    except Exception as e:
        print(e)
        flash('Hubo un error', 'error')
        return redirect(url_for('nav.clientes'))
    
    return render_template('clientes.html')



       