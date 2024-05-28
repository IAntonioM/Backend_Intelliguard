from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.usuario import BaseDatosUsuarios
from utils.role_decorador import role_required
from flask_jwt_extended import jwt_required
import bcrypt

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')

    # Crear una nueva instancia de la base de datos para cada solicitud
    base_datos_usuarios = BaseDatosUsuarios("basededatos.db")

    # Buscar el usuario en la base de datos
    usuario_db = base_datos_usuarios.consultar_usuario_por_usuario(usuario)
    if usuario_db and bcrypt.checkpw(contraseña.encode('utf-8'), usuario_db.hash_contraseña):
        # Si las contraseñas coinciden, generar el token JWT
        additional_claims = {"rol": usuario_db.rol}
        access_token = create_access_token(identity=usuario,additional_claims=additional_claims)
        # additional_claims = {"roles": usuario_db.}
        return jsonify({'access_token': access_token,'username':usuario_db.usuario,'roel':usuario_db.rol}), 200
    else:
        return jsonify({'mensaje': 'Credenciales incorrectas'}), 401



@auth_bp.route('/registro', methods=['POST'])
@jwt_required()
@role_required('Administrador')
def registro():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')
    idRol = data.get('idRol')

    # Crear una nueva instancia de la base de datos para cada solicitud
    base_datos_usuarios = BaseDatosUsuarios("basededatos.db")

    # Verificar si el usuario ya existe en la base de datos
    if base_datos_usuarios.consultar_usuario_por_usuario(usuario):
        return jsonify({'mensaje': 'El usuario ya existe'}), 400

    hash_contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
    base_datos_usuarios.agregar_usuario(usuario, hash_contraseña, idRol)

    return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 200
