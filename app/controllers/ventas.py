from flask import Blueprint, render_template, request, jsonify, json
from app.models.models import db, Compra, Cliente, Producto, Factura
import random
import string

venta = Blueprint('venta', __name__)

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