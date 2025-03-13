
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.models.models import db, Producto  
producto = Blueprint('producto', __name__)

# Registrar producto
@producto.route('/registrar_producto', methods=['POST'])
def registrar_producto():
    if request.method == 'POST':
        try:
            # Datos del formulario
            nombre = request.form.get('nombre')
            precio = request.form.get('precio')
            codigo = request.form.get('codigo')
            # Validación
            if not (nombre and precio and codigo):
                flash('Datos inválidos', 'error')
                return redirect(url_for('nav.productos'))
            # Registrar producto
            producto = Producto(nombre = nombre, precio = precio, codigo = codigo)
            db.session.add(producto)
            db.session.commit()
            flash('El producto se ha registrado', 'success')
            return redirect (url_for('nav.productos'))
        except Exception as e:
            db.session.rollback()
            print(e)
            flash('Hubo un error. No se ha regisrado el producto.', 'error')
    return render_template('productos.html')




# Obtener información de un producto
@producto.route('/get_producto', methods=['GET'])
def get_producto():
    id = request.args.get('id')
    producto = Producto.query.filter_by(id = id).first()
    if producto:
        return jsonify(producto.to_dict()), 200
    else:
        return jsonify({'mensaje' : 'Producto no encontrado'}), 404

# Obtener información para barra de búsqueda
@producto.route('/get_producto_busqueda', methods=['GET'])
def get_producto_busqueda():
    dato_busqueda = request.args.get('producto')
    opcion_busqueda = request.args.get('opcion_busqueda')
    try:
        if opcion_busqueda == 'nombre':
            producto = Producto.query.filter_by(nombre = dato_busqueda).first()
            if producto:
                return jsonify(producto.to_dict())
            else:
                return jsonify({'mensaje': 'Producto no encontrado'}), 404
                
        if opcion_busqueda == 'codigo':
            producto = Producto.query.filter_by(codigo = dato_busqueda).first()
            if producto:
                return jsonify(producto.to_dict())
            else:
                return jsonify({'mensaje': 'Producto no encontrado'}), 404
        else:
            print('no se puede enviar la información')
            return jsonify({'mensaje':'error'})
    except Exception as e:
        print(e)

# Eliminar producto
@producto.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    try:
        producto_id = request.form['id']
        # Validación
        if not producto_id:
            flash('Producto no encontrado.', 'error')
        # Buscar cliente
        producto = Producto.query.filter_by(id = producto_id).first()
        if producto:
            # Eliminar cliente
            db.session.delete(producto)
            db.session.commit()
            flash('El producto se ha eliminado.', 'success')
            return redirect(url_for('nav.productos'))
    except Exception as e:
        db.session.rollback()
        print(e)
        flash('Hubo un error.', 'error')
        return redirect(url_for('nav.productos'))

    return render_template('productos.html')




# Actualizar infromación de un producto
@producto.route('/actualizar_producto', methods=['POST'])
def actualizar_producto():
    try:
        # Datos del producto
        id = request.form.get('id_readonly')
        nombre = request.form.get('info_nombre')
        codigo = request.form.get('info_codigo')
        precio = request.form.get('info_precio')
        # Validación
        if not (id and nombre and codigo and precio):
            flash('Datos inválidos.', 'error')
            return redirect(url_for('nav.productos'))
        # Verificar producto
        producto = Producto.query.filter_by(id = id).first()
        if not producto:
            flash('Producto no encontrado.', 'error')
            return redirect(url_for('nav.productos'))
        # Actualizar los datos del producto
        producto.nombre = nombre
        producto.codigo = codigo
        producto.precio = precio
        db.session.commit()
        flash('Se han actualizado los datos del producto.', 'success')
        return redirect(url_for('nav.productos'))
    except Exception as e:
        db.session.rollback()
        print(e)
        flash('Hubo un error.', 'error')
        return redirect(url_for('nav.productos'))
    


    
