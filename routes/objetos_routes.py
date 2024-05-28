from flask import Blueprint, jsonify,request
from services.objetos_service import ObjetosServices
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.role_decorador import role_required

objetos_bp = Blueprint('objetos', __name__)


@objetos_bp.route('/objeto/reconocimiento-objeto', methods=['POST'])
@jwt_required()
@role_required('Personal')
def identificar_objeto():
    file = request.files['file']
    objeto=ObjetosServices.identificar_objeto(file)
    if objeto == -1:
        return jsonify({'error': 'No se Detecto el Tipo Objeto'}), 404
    else:
        return jsonify({
                'id':objeto.id_objeto,
                'objeto': objeto.nombre,
            }), 200
