from flask import Blueprint, render_template, request, jsonify
from app.models.models import db, Factura

factura = Blueprint('factura', __name__)


@factura.route('/get_facturas', methods=['GET'])
def get_facturas():
    facturas = Factura.query.all()
    return jsonify([factura.to_dict() for factura in facturas])


@factura.route('/info_factura', methods=['GET'])
def info_factura():
    id = request.args.get('id')
    factura = Factura.query.filter_by(id=id).first()
    if factura:
        return jsonify(factura.to_dict())
    else:
        return jsonify({"mensaje": "Factura no encontrada."}), 404
