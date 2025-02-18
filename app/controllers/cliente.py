from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models.models import db, Cliente, Compra, Factura
cliente = Blueprint('cliente', __name__)

# Registrar clientes
@cliente.route('/registrar_cliente', methods = ['POST'])
def registrar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        tipo_cliente = request.form['tcliente']

        try:
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
        cliente = Cliente.query.filter_by(id = cliente_id).first()
        if cliente:
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


@cliente.route('/info_cliente/<int:id>', methods = ['GET'])
def info_cliente(id):
    cliente = Cliente.query.filter_by(id = id).first()
    if cliente:
        return jsonify(cliente.to_dict())


@cliente.route('/get_clientes')
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([cliente.to_dict() for cliente in clientes]), 200

@cliente.route('/actualizar_cliente', methods = ['POST'])
def actualizar_cliente():
    datos = request.get_json()
    id = datos.get('id')
    nombre = datos.get('nombre')
    correo = datos.get('correo')
    telefono = datos.get('telefono')
    direccion = datos.get('direccion')
    cliente = Cliente.query.filter_by(id = id).first()
    if cliente:
        cliente.nombre = nombre
        cliente.correo = correo
        cliente.telefono = telefono
        cliente.direccion = direccion
        db.session.commit()
        return jsonify({"mensaje" : "Los datos se han actualizado."})
    else:
        return jsonify({"mensaje" : "Los datos no se han podido actualizar"}), 500