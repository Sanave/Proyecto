from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Date  
from datetime import date
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask import jsonify


db = SQLAlchemy()


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
    # Cliente - Compra
    compras = db.relationship('Compra', backref = 'cliente', cascade="all, delete")
    # Cliente - Factura
    facturas = db.relationship('Factura', backref ='cliente', cascade="all, delete")
    

    def to_dict(self):
        return {
            "id" : self.id,
            "nombre" : self.nombre,
            "direccion" : self.direccion,
            "telefono" : self.telefono,
            "correo" : self.correo,
            "tipo_cliente" : self.tipo_cliente,
            "estado" : self.estado,
           # "compras" : [compra.id for compra in self.compras],
            #"facturas" : [factura.id for factura in self.facturas]
        }

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(150), nullable = False)
    precio = db.Column(db.Integer, nullable = False)
    codigo = db.Column(db.String(150), nullable = False, unique = True)
    # Producto - Compra
    compras = db.relationship('CompraProducto', backref='producto')
    # Factura - Productos
    facturas = db.relationship('FacturaProducto', backref='producto')

    def to_dict(self):
        return {
            "id" : self.id,
            "nombre" : self.nombre,
            "precio" : self.precio,
            "codigo" : self.codigo,
        }

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    numero_factura = db.Column(db.String(150), nullable = False, unique = True)
    fecha_emision = db.Column(db.Date, default=func.current_date())
    total = db.Column(db.Integer, nullable = False)
    # Cliente -Factura
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable = False)
    # Compra - Factura
    id_compra = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=True)
    # Factura - Productos
    productos = db.relationship('FacturaProducto', backref='factura', cascade="all, delete")

    def to_dict(self):
        return {
            "id" : self.id,
            "numero_factura" : self.numero_factura,
            "fecha_emision" : self.fecha_emision,
            "total" : self.total,
            "id_cliente" : self.id_cliente,
            "id_compra" : self.id_compra,
            "cliente": self.cliente.to_dict() if self.cliente else None,
            "productos": [producto.to_dict() for producto in self.productos]
        }

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha_venta = db.Column(db.Date, nullable=False, default=func.current_date())
    total = db.Column(db.Integer, nullable = False)
    # Cliente - Compra
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable = False)
    # Compra - Producto
    productos = db.relationship('CompraProducto', backref='compra', cascade="all, delete")
    # Compra - factura
    factura = db.relationship('Factura', backref='compra', uselist=False, cascade="all, delete")

    def to_dict(self):
        return {
            "id" : self.id,
            "fecha_venta" : self.fecha_venta,
            "total" : self.total,
            "id_cliente" : self.id_cliente,
            "cliente": self.cliente.to_dict() if self.cliente else None,
            #"factura" : self.factura.id if self.factura else None,
            "productos": [
                {
                "id": cp.producto.id,
                "nombre": cp.producto.nombre,
                "precio": cp.producto.precio,
                "codigo": cp.producto.codigo,  
                "cantidad": cp.cantidad,  
                "subtotal": cp.cantidad * cp.producto.precio  
                }
                for cp in self.productos 
            ]
        }

class Vendedor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(150), nullable = False)
    direccion = db.Column(db.String(150), nullable = False)
    telefono = db.Column(db.String(15), nullable = False)
    correo = db.Column(db.String(150), nullable = False, unique = True)

    def to_dict(self):
        return{
            "id" : self.id,
            "nombre" : self.nombre,
            "direccion" : self.direccion,
            "telefono" : self.telefono,
            "correo" : self.correo
        }


# Tabla intermedia Compra - Producto
class CompraProducto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id', ondelete="CASCADE"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)

# Tabla intermedia Factura - Producto
class FacturaProducto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)

    def to_dict(self):
        return{
            "id": self.id,
            "factura_id": self.factura_id,
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
            "producto": self.producto.to_dict() if self.producto else None
        }


    
