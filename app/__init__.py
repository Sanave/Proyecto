from flask import Flask
from config import Config
from .models.models import db, Usuario



def create_app():
    app = Flask (__name__)
    app.config.from_object(Config)
    db.init_app(app)




    from .controllers.nav import nav
    from .controllers.cliente import cliente
    from .controllers.producto import producto
    from .controllers.ventas import venta
    from .controllers.facturas import factura
    from .controllers.aut import aut
    app.register_blueprint(aut, url_prefix = '/')
    app.register_blueprint(factura, url_prefix = '/')
    app.register_blueprint(venta, url_prefix = '/')
    app.register_blueprint(producto, url_prefix = '/')
    app.register_blueprint(nav, url_prefix = '/')
    app.register_blueprint(cliente, url_prefix = '/')
    with app.app_context():
        db.create_all()


    return app