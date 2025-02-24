from flask import Blueprint, render_template, request
from app.models.models import Cliente, Producto, Factura, Compra
nav = Blueprint('nav', __name__)

@nav.route('/')
def index():
    return render_template('login.html')

@nav.route('/signup')
def signup():
    return render_template('signup.html')

@nav.route('/login')
def login():
    return render_template('login.html')

@nav.route('/clientes')
def clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes = clientes)

@nav.route('/productos')
def productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos = productos)

@nav.route('/facturas')
def facturas():
    facturas = Factura.query.all()
    return render_template('facturas.html', facturas = facturas)

@nav.route('/compras')
def compras():
    clientes = Cliente.query.all()
    productos = Producto.query.filter_by(disponible=True).all()
    compras = Compra.query.all()
    return render_template('compras.html', clientes = clientes, productos = productos, compras = compras)

@nav.route('/infocliente/<id>', methods = ['GET'])
def infocliente(id):
    cliente = Cliente.query.filter_by( id = id).first()
    return render_template('infocliente.html', cliente = cliente)

@nav.route('/infoproducto/<id>', methods = ['GET'])
def infoproducto(id):
    producto = Producto.query.filter_by(id=id).first()
    return render_template('infoproducto.html', producto = producto)

@nav.route('/venta', methods = ['GET', 'POST'])
def venta():
    id = request.form['id_venta']
    return render_template('venta.html', id = id)
