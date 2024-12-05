from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Date  
from datetime import date
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask import jsonify


db = SQLAlchemy()



compra_producto = db.Table('compra_producto', 
    db.Column('compra_id', db.Integer, db.ForeignKey('compra.id'), primary_key=True),
    db.Column('producto_id', db.Integer, db.ForeignKey('producto.id'), primary_key=True)
)

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(150), nullable = False)
    correo = db.Column(db.String(150), nullable = False, unique = True)
    contrasena = db.Column(db.String(150), nullable = False)

    def to_dict(self):
        return {
            "id" : self.id,
            "nombre" : self.nombre,
            "correo" : self.correo
        }
        
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(150), nullable = False)
    direccion = db.Column(db.String(150), nullable = False)
    telefono = db.Column(db.String(15), nullable = False)
    correo = db.Column(db.String(150), nullable = False, unique = True)
    tipo_cliente = db.Column(db.String(20), nullable = False)
    estado = db.Column(db.String(25), nullable = False)
    compras = db.relationship('Compra', backref = 'cliente', lazy = True, cascade="all, delete-orphan")
    facturas = db.relationship('Factura', backref = 'cliente', lazy = True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id" : self.id,
            "nombre" : self.nombre,
            "direccion" : self.direccion,
            "telefono" : self.telefono,
            "correo" : self.correo,
            "tipo_cliente" : self.tipo_cliente,
            "estado" : self.estado,
            "compras" : [compra.id for compra in self.compras],
            "facturas" : [factura.id for factura in self.facturas]
        }

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(150), nullable = False)
    precio = db.Column(db.Integer, nullable = False)
    codigo = db.Column(db.String(150), nullable = False, unique = True)
    disponible = db.Column(db.Boolean, default = True)
    compras = db.relationship('Compra', secondary=compra_producto, backref=db.backref('productos_compra', lazy='dynamic'))

    def to_dict(self):
        return {
            "id" : self.id,
            "nombre" : self.nombre,
            "precio" : self.precio,
            "codigo" : self.codigo,
            "disponible" : self.disponible,
            "compras" : [compra.id for compra in self.compras]
        }

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    numero_factura = db.Column(db.String(150), nullable = False, unique = True)
    fecha_emision = db.Column(db.Date, default=func.current_date())
    total = db.Column(db.Integer, nullable = False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable = False)
    id_compra = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=True)

    def to_dict(self):
        return {
            "id" : self.id,
            "numero_factura" : self.numero_factura,
            "fecha_emision" : self.fecha_emision,
            "total" : self.total,
            "id_cliente" : self.id_cliente,
            "id_compra" : self.id_compra
        }

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha_venta = db.Column(db.Date, nullable=False, default=func.current_date())
    total = db.Column(db.Integer, nullable = False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable = False)
    factura = db.relationship('Factura', backref='compra', uselist=False, cascade="all, delete-orphan")
    productos = db.relationship('Producto', secondary=compra_producto, backref=db.backref('compras_producto', lazy='dynamic'))

    def to_dict(self):
        return {
            "id" : self.id,
            "fecha_venta" : self.fecha_venta,
            "total" : self.total,
            "id_cliente" : self.id_cliente,
            "factura" : self.factura.id if self.factura else None,
            "productos" : [producto.id for producto in self.productos]
        }


    
