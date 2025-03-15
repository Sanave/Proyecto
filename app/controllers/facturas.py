from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.models.models import *
from flask_login import login_required
import uuid

factura = Blueprint('factura', __name__)

# Crear factura
@factura.route('/crear_factura', methods=['POST'])
@login_required
def crear_factura():
    try:
        id_compra = request.form.get('id_compra')

        # Obtener la compra y cliente
        compra = Compra.query.get(id_compra)
        id_cliente = compra.id_cliente
        cliente = Cliente.query.get(id_cliente)

        # Obtener los productos de la compra
        productos_compra = CompraProducto.query.filter_by(compra_id=id_compra).all()
        
        # Calcular total de la factura
        total_factura = sum(cp.producto.precio * cp.cantidad for cp in productos_compra)
        
        # Generar número de factura
        numero_factura = str(uuid.uuid4())[:8]

        # Crear la factura
        factura = Factura(numero_factura=numero_factura, id_cliente=id_cliente, id_compra=id_compra, total=total_factura)
        db.session.add(factura)
        db.session.flush()

        # Agregar productos a la factura
        for cp in productos_compra:
            factura_producto = FacturaProducto(factura_id=factura.id, producto_id=cp.producto_id, cantidad=cp.cantidad)
            db.session.add(factura_producto)

        db.session.commit()
        flash('Factura Guardada', 'success')
        return redirect(url_for('nav.facturas'))

    except Exception as e:
        print(e)
        db.session.rollback()
        flash('Hubo un error.', 'error')
        return redirect(url_for('nav.facturas'))


@factura.route('/get_factura', methods=['GET'])
@login_required
def get_factura():
    try:
        id_factura = request.args.get('id')
        if not id_factura:
            return jsonify({'mensaje' : 'Hubo un error al recibir el id del cliente'}, 500)
        factura = Factura.query.filter_by(id = id_factura).first()
        if not factura:
            return jsonify({'mensaje' : 'No se ha encontrado la factura.'}), 404
        return jsonify(factura.to_dict()), 200
    except Exception as error:
        print(error)
        

@factura.route('/get_facturas', methods=['GET'])
@login_required
def get_facturas():
    facturas = Factura.query.all()
    return jsonify([factura.to_dict() for factura in facturas])