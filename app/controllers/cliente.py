from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models.models import db, Cliente, Compra, Factura
cliente = Blueprint('cliente', __name__)

# Registrar clientes
@cliente.route('/registrar_cliente', methods = ['POST'])
def registrar_cliente():
    if request.method == 'POST':
        # Datos del formulario
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        tipo_cliente = request.form['tcliente']

        try:
            # Registrar cliente
            cliente = Cliente(nombre = nombre, correo = correo, telefono = telefono, direccion = direccion, tipo_cliente = tipo_cliente, estado = 'activo')
            db.session.add(cliente)
            db.session.commit()
            flash('El cliente se ha registrado.', 'success')
            return redirect(url_for('nav.clientes'))
        except Exception as e:
            db.session.rollback()
            print(e)
            flash('Hubo un error. No se ha registrado el cliente.')
    return render_template('clientes.html')


# Eliminar clientes
@cliente.route('/eliminar_cliente', methods=['POST'])
def eliminar_cliente():
    cliente_id = request.form['id']
   
    try:
        # Buscar cliente en BD
        cliente = Cliente.query.filter_by(id = cliente_id).first()
        if cliente:
            # Eliminar el cliente
            db.session.delete(cliente)
            db.session.commit()
            flash('El cliente se ha eliminado', 'success')
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
        return jsonify(cliente.to_dict())
    else:
        print('El cliente no existe')


# Actualizar información de un cliente
@cliente.route('/actualizar_cliente', methods = ['POST'])
def actualizar_cliente():
    id = request.form.get('id_readonly')
    print('idd' + id)
    nombre = request.form.get('info_nombre')
    correo = request.form.get('info_correo')
    telefono = request.form.get('info_telefono')
    direccion = request.form.get('info_direccion')
    tcliente = request.form.get('info_tcliente')
    cliente = Cliente.query.filter_by(id = id).first()
    if cliente:
        try:
            cliente.nombre = nombre
            cliente.correo = correo
            cliente.telefono = telefono
            cliente.direccion = direccion
            cliente.tipo_cliente = tcliente
            db.session.commit()
            flash('Se han actualizado los datos del cliente.', 'success')
            return redirect(url_for('nav.clientes'))
        except Exception as e:
            print(e)
            flash('Hubo un error', 'error')
            return redirect(url_for('nav.clientes'))
    else:
        flash('Cliente no encontrado.', 'error')
        return redirect(url_for('nav.clientes'))
    
    return render_template('clientes.html')


    '''@cliente.route('/info_cliente/<int:id>', methods = ['GET'])
def info_cliente(id):
    cliente = Cliente.query.filter_by(id = id).first()
    if cliente:
        return jsonify(cliente.to_dict())'''
       