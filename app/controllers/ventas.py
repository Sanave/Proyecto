from flask import Blueprint, render_template, request, jsonify
from app.models.models import db, Compra, Cliente, Producto, Factura
import random
import string

venta = Blueprint('venta', __name__)

@venta.route('get_producto', methods = ['GET'])
def get_producto():
    id = request.args.get('id')
    producto = Producto.query.filter_by(id = id).first()
    if producto:
        return jsonify(producto.to_dict())


@venta.route('/registrar_venta', methods=['POST'])
def registrar_venta():
    data = request.get_json()

    productos_ids = data.get('productos', [])
    cliente_id = data.get('id_cliente')
    total_venta = data.get('total')

    cliente = Cliente.query.get(cliente_id)
    productos = Producto.query.filter(Producto.id.in_(productos_ids)).all()

    compra = Compra(total=total_venta, id_cliente=cliente_id)
    db.session.add(compra)
    db.session.commit()

    compra.productos = productos
    db.session.commit()


    numero_factura = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    factura = Factura(numero_factura=numero_factura, total=total_venta, id_cliente=cliente_id, id_compra=compra.id)
    db.session.add(factura)
    db.session.commit()

    return jsonify({"mensaje": "Venta registrada con éxito", "factura": factura.to_dict()}), 201