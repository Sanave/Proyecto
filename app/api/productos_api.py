from flask_restful import Resource
from flask import request, jsonify
from flask_cors import cross_origin
from app.models.models import db, Producto

class ProductosApi(Resource):
    # Este decorador lanza error en la API.
   # @cross_origin (Supuestamente no es necesario. CORS(app) se aplica globalmente a toda la aplicación.)
    def post (self):
       producto = Producto(nombre = request.json['nombre'], codigo = request.json['codigo'], precio = request.json['precio'])
       db.session.add(producto)
       db.session.commit()
       return jsonify({"mensaje" : "producto guardado"})
    
    def get(self):
        productos = Producto.query.all()
        productos_dict = []
        for producto in productos:
            productos_dict.append({
                'id' : producto.id,
                'nombre' : producto.nombre,
                'codigo' : producto.codigo,
                'precio' : producto.precio
            })
        return jsonify(productos_dict)