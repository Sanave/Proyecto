
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.models.models import db, Producto  
producto = Blueprint('producto', __name__)

# Registrar producto
@producto.route('/registrar_producto', methods=['POST'])
def registrar_producto():
    if request.method == 'POST':
        # Datos del formulario
        nombre = request.form['nombre']
        precio = request.form['precio']
        codigo = request.form['codigo']

        try:
            # Registrar producto
            producto = Producto(nombre = nombre, precio = precio, codigo = codigo)
            db.session.add(producto)
            db.session.commit()
            flash('El producto se ha registrado', 'success')
            return redirect (url_for('nav.productos'))
        except Exception as e:
            db.session.rollback()
            print(e)
            flash('Hubo un error, no se ha regisrado el producto.', 'error')
    return render_template('productos.html')




# Obtener información de un producto
@producto.route('/get_producto', methods=['GET'])
def get_producto():
    id = request.args.get('id')
    producto = Producto.query.filter_by(id = id).first()
    if producto:
        return jsonify(producto.to_dict())
    else:
        print('El producto no existe')


# Eliminar producto
@producto.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    producto_id = request.form['id']

    try:
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
    # Datos del producto
    id = request.form['id_readonly']
    nombre = request.form['info_nombre']
    codigo = request.form['info_codigo']
    precio = request.form['info_precio']
    producto = Producto.query.filter_by(id = id).first()

    try:
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
    


    
