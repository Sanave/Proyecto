from flask import Blueprint, render_template, request, jsonify
from app.models.models import *
import uuid

factura = Blueprint('factura', __name__)

# Crear factura
@factura.route('/crear_factura', methods=['POST'])
def crear_factura():
    try:
        id_compra = request.form.get('id_compra')

        # Obtener la compra y cliente
        compra = Compra.query.get(id_compra)
        id_cliente = compra.id_cliente
        cliente = Cliente.query.get(id_cliente)  # No es obligatorio para registrar la factura

        # Obtener los productos de la compra
        productos_compra = CompraProducto.query.filter_by(compra_id=id_compra).all()
        
        # Calcular total de la factura
        total_factura = sum(cp.producto.precio * cp.cantidad for cp in productos_compra)
        
        # Generar número de factura único
        numero_factura = str(uuid.uuid4())[:8]

        # Crear la factura
        factura = Factura(numero_factura=numero_factura, id_cliente=id_cliente, id_compra=id_compra, total=total_factura)
        db.session.add(factura)
        db.session.flush()  # Permite obtener el id de la factura antes de commit

        # Agregar productos a la factura
        for cp in productos_compra:
            factura_producto = FacturaProducto(factura_id=factura.id, producto_id=cp.producto_id, cantidad=cp.cantidad)
            db.session.add(factura_producto)

        db.session.commit()  # Guardar cambios en la BD

        return "Factura creada", 201

    except Exception as e:
        print(e)
        db.session.rollback()  # Deshacer cambios si hay error
        return "Error al crear la factura", 500





@factura.route('/get_facturas', methods=['GET'])
def get_facturas():
    facturas = Factura.query.all()
    return jsonify([factura.to_dict() for factura in facturas])


@factura.route('/info_factura', methods=['GET'])
def info_factura():
    id = request.args.get('id')
    factura = Factura.query.filter_by(id=id).first()
    if factura:
        return jsonify(factura.to_dict())
    else:
        return jsonify({"mensaje": "Factura no encontrada."}), 404
