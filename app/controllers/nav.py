from flask import Blueprint, render_template, request, redirect, url_for
from app.models.models import Cliente, Producto, Factura, Compra, Vendedor
from flask_login import login_required
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
@login_required
def clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes = clientes)

@nav.route('/productos')
@login_required
def productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos = productos)

@nav.route('/facturas')
@login_required
def facturas():
    facturas = Factura.query.all()
    return render_template('facturas.html', facturas = facturas)

@nav.route('/compras')
@login_required
def compras():
    clientes = Cliente.query.all()
    productos = Producto.query.all()
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
@login_required
def venta():
    id = request.form['id_venta']
    cliente = Cliente.query.filter_by( id = id ).first()
    productos = Producto.query.all()
    if not cliente:
        redirect(url_for('nav.clientes'))
    return render_template('venta.html', cliente = cliente, productos = productos)

@nav.route('/vendedores')
@login_required
def vendedores():
    vendedores = Vendedor.query.all()
    return render_template('vendedores.html', vendedores = vendedores)

