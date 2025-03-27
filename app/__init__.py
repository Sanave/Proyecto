from flask import Flask
from config import Config
from .models.models import db, Usuario
from flask_login import LoginManager
from flask_cors import CORS
from flask_restful import Api
from app.api.productos_api import ProductosApi





def create_app():
    app = Flask (__name__)

    app.config.from_object(Config)
    db.init_app(app)

    api = Api(app)
    api.add_resource(ProductosApi, '/api/productos')
    CORS(app)
# Login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'aut.registro'

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))



# Registro de Blueprints
    from .controllers.nav import nav
    from .controllers.cliente import cliente
    from .controllers.producto import producto
    from .controllers.ventas import venta
    from .controllers.facturas import factura
    from .controllers.aut import aut
    from .controllers.vendedores import vendedor

    app.register_blueprint(aut, url_prefix = '/')
    app.register_blueprint(factura, url_prefix = '/')
    app.register_blueprint(venta, url_prefix = '/')
    app.register_blueprint(producto, url_prefix = '/')
    app.register_blueprint(nav, url_prefix = '/')
    app.register_blueprint(cliente, url_prefix = '/')
    app.register_blueprint(vendedor, url_prefix = '/')
    # Crear base de datos
    with app.app_context():
        db.create_all()


    return app