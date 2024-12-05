
from flask import Blueprint, render_template, request, jsonify
from app.models.models import db, Producto  
producto = Blueprint('producto', __name__)

@producto.route('/registrar_producto', methods=['POST'])
def registrar_producto():
    if request.method == 'POST':
        datos = request.get_json()
        nombre = datos.get('nombre')
        precio = datos.get('precio')
        codigo = datos.get('codigo')

        try:
            producto = Producto(nombre=nombre, precio=precio, codigo=codigo)
            db.session.add(producto)
            db.session.commit()
            return jsonify({"mensaje": "Producto registrado."})
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return jsonify({"mensaje": "No se pudo registrar el producto."}), 500

@producto.route('/get_productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    return jsonify([producto.to_dict() for producto in productos])

@producto.route('/info_producto/<int:id>', methods=['GET'])
def info_producto(id):
    producto = Producto.query.filter_by(id=id).first()
    if producto:
        return jsonify(producto.to_dict())

@producto.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    datos = request.get_json()
    id = datos.get('id')
    producto = Producto.query.filter_by(id=id).first()

    try:
        db.session.delete(producto)
        db.session.commit()
        return jsonify({"mensaje": "El producto se ha eliminado."})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"mensaje": "Error al eliminar producto."}), 500

@producto.route('/actualizar_producto', methods=['POST'])
def actualizar_producto():
    datos = request.get_json()
    id = datos.get('id')
    nombre = datos.get('nombre')
    precio = datos.get('precio')
    codigo = datos.get('codigo')
    
    producto = Producto.query.filter_by(id=id).first()

    if producto:
        producto.nombre = nombre
        producto.precio = precio
        producto.codigo = codigo
        db.session.commit()
        return jsonify({"mensaje": "El producto se ha actualizdo."})
    else:
        return jsonify({"mensaje": "Producto no encontrado."}), 404

@producto.route('/get_producto_data/<int:id>/<int:cantidad>')
def get_producto_data(id, cantidad):
    producto = Producto.query.get(id) 
    if producto:

        producto_data = {
            "nombre": producto.nombre,
            "precio": producto.precio,
            "codigo": producto.codigo,
            "total": producto.precio * cantidad
        }
        return jsonify(producto_data)
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404


    
