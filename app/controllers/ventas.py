from flask import Blueprint, render_template, request, jsonify, flash, json
from app.models.models import db, Compra, Cliente, Producto, Factura, CompraProducto
import random
import string
from sqlalchemy.sql import func

venta = Blueprint('venta', __name__)

# Confirmacion de para pantalla de venta
@venta.route('venta_confirmacion', methods = ['GET'])
def venta_confirmacion():
    id_cliente = request.args.get('cliente')
    carrito = request.args.get('carrito')
    carrito = json.loads(carrito)
    try:
        cliente = Cliente.query.filter_by(id = id_cliente).first()
        productos = {}
        total = 0
        for id_producto, cantidad in carrito.items():
            producto = Producto.query.filter_by(id = id_producto).first()
            if producto:
                producto_datos = producto.to_dict()
                producto_datos['cantidad'] = cantidad
                producto_datos['cantidad_total'] = producto.precio * cantidad
                productos[id_producto] = producto_datos
                total += producto.precio * cantidad
            else:
                print('Producto no encontrado')
        print(productos)
        return jsonify({
            "cliente" : cliente.to_dict(),
            "productos" : productos,
            "total" : total
        })
    except Exception as e:
        print(e)

# Obtener información de compra
@venta.route('get_compra', methods = ['GET'])
def get_compra():
    id_compra = request.args.get('id')
    try:
        compra = Compra.query.filter_by(id = id_compra).first()
        if not compra:
            return jsonify({"mensaje" : "No se ha encontrado la compra."}), 404
        return jsonify(compra.to_dict())
    except Exception as error:
        print(error)






@venta.route('get_producto', methods = ['GET'])
def get_producto():
    id = request.args.get('id')
    producto = Producto.query.filter_by(id = id).first()
    if producto:
        return jsonify(producto.to_dict())

# Registrar venta (pendiente)---------------------------------------------------------------
@venta.route('/registrar_venta', methods=['POST'])
def registrar_compra():
    data = request.json
    cliente_id = data.get('id_cliente')
    productos = data.get('productos')  # {producto_id: cantidad}

    if not cliente_id or not productos:
        return jsonify({"error": "Se requiere id_cliente y productos"}), 400

    # Verificar que el cliente existe
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        print('cliente no encontrado')
        return jsonify({"error": "Cliente no encontrado"}), 404

    # Crear la compra
    compra = Compra(id_cliente=cliente.id, fecha_venta=func.current_date(), total=0)
    db.session.add(compra)
    db.session.flush()  # Asegura que compra.id esté disponible antes de commit

    total_compra = 0  # Calcular el total de la compra

    for producto_id, cantidad in productos.items():
        producto = Producto.query.get(producto_id)
        if not producto:
            print('producto no encontrado')
            return jsonify({"error": f"Producto con ID {producto_id} no encontrado"}), 404

        # Crear relación en CompraProducto
        compra_producto = CompraProducto(compra_id=compra.id, producto_id=producto.id, cantidad=cantidad)
        db.session.add(compra_producto)

        # Calcular el total de la compra
        total_compra += producto.precio * cantidad

    # Actualizar total de la compra
    compra.total = total_compra
    db.session.commit()

    return jsonify({"message": "Compra registrada con éxito", "compra_id": compra.id}), 201
   