from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.models import db, Cliente, Compra, Factura
cliente = Blueprint('cliente', __name__)

@cliente.route('/registrar_cliente', methods = ['GET','POST'])
def registrar_cliente():
    if request.method == 'POST':
        datos = request.get_json()
        nombre = datos.get('nombre')
        correo = datos.get('correo')
        telefono = datos.get('telefono')
        direccion = datos.get('direccion')
        tipo_cliente = datos.get('tipo_cliente')

        try:
            cliente = Cliente(nombre = nombre, correo = correo, telefono = telefono, direccion = direccion, tipo_cliente = tipo_cliente, estado = 'activo')
            db.session.add(cliente)
            db.session.commit()
            return jsonify({"mensaje" : "El cliente se ha registrado."})
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return jsonify({"mensaje" : "El cliente no se ha podido registrar."})   

@cliente.route('/eliminar_cliente', methods=['POST'])
def eliminar_cliente():
    datos = request.get_json()
    id = datos.get('id')
    cliente = Cliente.query.filter_by(id = id).first()
    
    try:
        for compra in cliente.compras:
            compra.productos = []  
            db.session.delete(compra)  
        for factura in cliente.facturas:
            db.session.delete(factura) 
        db.session.delete(cliente)
        db.session.commit() 
        
        return jsonify({"mensaje" : "cliente eliminado"})
    
    except Exception as e:
        db.session.rollback() 
        print(f"depuración: {e}")


@cliente.route('/info_cliente/<int:id>', methods = ['GET'])
def info_cliente(id):
    cliente = Cliente.query.filter_by(id = id).first()
    if cliente:
        return jsonify(cliente.to_dict())


@cliente.route('/get_clientes')
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([cliente.to_dict() for cliente in clientes])

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