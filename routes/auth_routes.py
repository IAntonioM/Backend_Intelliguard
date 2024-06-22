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
    base_datos_usuarios = BaseDatosUsuarios("basededatos.db")
    usuario_db = base_datos_usuarios.consultar_usuario_por_usuario(usuario)
    if usuario_db and bcrypt.checkpw(contraseña.encode('utf-8'), usuario_db.hash_contraseña):
        additional_claims = {"rol": usuario_db.rol}
        access_token = create_access_token(identity=usuario,additional_claims=additional_claims)
        return jsonify({'access_token': access_token}), 200
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
    base_datos_usuarios = BaseDatosUsuarios("basededatos.db")
    if base_datos_usuarios.consultar_usuario_por_usuario(usuario):
        return jsonify({'mensaje': 'El usuario ya existe'}), 400
    hash_contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
    base_datos_usuarios.agregar_usuario(usuario, hash_contraseña, idRol)
    return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 200

@auth_bp.route('/usuarios', methods=['POST'])
@jwt_required()
@role_required('Administrador')
def listar_usuarios():
    try:
        base_datos_usuarios = BaseDatosUsuarios("basededatos.db")
        usuarios = base_datos_usuarios.listar_usuarios()
        usuarios_json = []
        for usuario in usuarios:
            usuarios_json.append({
                'id': usuario.id_usuario,
                'nombre': usuario.usuario,
                'rol': usuario.rol
            })
        return jsonify({'usuarios': usuarios_json}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
@jwt_required()
@role_required('Administrador') 
def eliminar_usuario(id_usuario):
    try:
        base_datos_usuarios = BaseDatosUsuarios("basededatos.db")
        base_datos_usuarios.eliminar_usuario(id_usuario)
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/usuarios/<int:id_usuario>', methods=['PUT'])
@jwt_required()
@role_required('Administrador') 
def editar_usuario(id_usuario):
    base_datos_usuarios = BaseDatosUsuarios("basededatos.db")
    datos_usuario = request.json
    nuevo_usuario = datos_usuario.get('usuario')
    nueva_contraseña = datos_usuario.get('contraseña')
    nuevo_id_rol = datos_usuario.get('idRol')
    if nueva_contraseña!="":
        nueva_contraseña = bcrypt.hashpw(nueva_contraseña.encode('utf-8'), bcrypt.gensalt())
    base_datos_usuarios.editar_usuario(id_usuario, nuevo_usuario, nueva_contraseña, nuevo_id_rol)
    return jsonify({'mensaje': 'Usuario editado exitosamente'}), 200
