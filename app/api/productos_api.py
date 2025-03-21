from flask_restful import Resource
from flask import request
from flask_cors import cross_origin
from app.models.models import db, Producto

class productosApi(Resource):
    @cross_origin
    def post (self):
        nombre = request.json['nombre']
        precio = request.json['precio']
        codigo = request.json['codigo']
        producto = Producto(nombre = nombre, precio = precio, codigo = codigo)
        db.session.add(producto)
        db.session.commit()
        return 'Producto guardado.'