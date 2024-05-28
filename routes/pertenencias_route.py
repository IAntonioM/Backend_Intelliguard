
from services.pertenencias_service import PertenenciasServices
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, Blueprint, jsonify, request, send_from_directory
import os
from flask import current_app, send_from_directory
import base64
from utils.role_decorador import role_required


pertenencias_bp = Blueprint('pertenencias', __name__)

@pertenencias_bp.route('/pertenencia/registrar-pertenencia', methods=['POST'])
@jwt_required()
@role_required('Personal')
def regsitrar_pertenencia():
    idEstudiante = request.form.get('idEstudiante')
    id_objeto = request.form.get('idObjeto')
    imgPertenencia = request.files['file']
    
    if not idEstudiante or not id_objeto or not imgPertenencia:
        return jsonify({'error': 'Faltan datos en la solicitud'}), 400

    try:
        PertenenciasServices.registrar_pertenencia(idEstudiante, id_objeto, imgPertenencia)
        return jsonify({'message': 'Registro exitoso'}), 200
    except Exception as e:
        return jsonify({'message': 'Error al Registrar Pertencia'}), 500
    
@pertenencias_bp.route('/pertenencia/consultar-pertenencia', methods=['POST'])
@jwt_required()
@role_required('Personal')
def consultar_pertenencia_por_id():
    idEstudiante = request.form.get('idEstudiante')
    idEstado = request.form.get('idEstado')
    UPLOAD_FOLDER = 'uploads/pertenencia'
    # Validar que el código del estudiante no esté vacío
    if not idEstudiante:
        return jsonify({'error': 'El código del estudiante es requerido'}), 400

    try:
        pertenencias = PertenenciasServices.consultar_pertencia_por_idEstudiante(idEstudiante, idEstado)
        if pertenencias == -1:
            return jsonify({'error': 'No hay pertenencias registradas del estudiante'}), 404
        else:
            # Formatear la respuesta JSON con la lista de pertenencias
            pertenencias_json = []
            for pertenencia in pertenencias:
                # Obtener la ruta completa de la imagen
                imagen_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, pertenencia.imagen_pertenencia)

                # Codificar la imagen en base64
                with open(imagen_path, 'rb') as imagen_file:
                    imagen_base64 = base64.b64encode(imagen_file.read()).decode('utf-8')

                pertenencias_json.append({
                    'idPertenencia': pertenencia.id_pertenencia,
                    'idEstudiante': pertenencia.id_estudiante,
                    'idObjeto': pertenencia.id_objeto,
                    'Fecha': pertenencia.fecha,
                    'nombreObjeto' : pertenencia.nombre_objeto,
                    'nombresEstudiante' : pertenencia.nombres_estudiante,
                    'ImagenPertenencia': f'data:image/jpeg;base64,{imagen_base64}',
                })

            return jsonify({'pertenencias': pertenencias_json}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@pertenencias_bp.route('/pertenencia/consultar-pertenencia-busqueda', methods=['POST'])
@jwt_required()
@role_required('Personal')
def consultar_pertenencia_por_busqueda():
    busqueda = request.form.get('busqueda')
    UPLOAD_FOLDER = 'uploads/pertenencia'
    if not busqueda:
        busqueda=''

    try:
        pertenencias = PertenenciasServices.consultar_pertencia_por_busqueda(busqueda)
        if pertenencias == -1:
            return jsonify({'error': 'Sin restulados de Busqueda ...'}), 404
        else:
            # Formatear la respuesta JSON con la lista de pertenencias
            pertenencias_json = []
            for pertenencia in pertenencias:
                # Obtener la ruta completa de la imagen
                imagen_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, pertenencia.imagen_pertenencia)

                # Codificar la imagen en base64
                with open(imagen_path, 'rb') as imagen_file:
                    imagen_base64 = base64.b64encode(imagen_file.read()).decode('utf-8')

                pertenencias_json.append({
                    'idPertenencia': pertenencia.id_pertenencia,
                    'idEstudiante': pertenencia.id_estudiante,
                    'idObjeto': pertenencia.id_objeto,
                    'idEstado': pertenencia.id_estado,
                    'Estado': pertenencia.estado,
                    'Fecha': pertenencia.fecha,
                    'nombreObjeto' : pertenencia.nombre_objeto,
                    'nombresEstudiante' : pertenencia.nombres_estudiante,
                    'ImagenPertenencia': f'data:image/jpeg;base64,{imagen_base64}',
                })

            return jsonify({'pertenencias': pertenencias_json}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para registrar la salida de una pertenencia
@pertenencias_bp.route('/pertenencia/registrar-salida-pertenencia', methods=['POST'])
@jwt_required()
@role_required('Personal')
def registrar_salida_pertenencia():
    # Obtener la lista de pertenencias del cuerpo de la solicitud
    pertenencias = request.json  # Se asume que se envía la lista de pertenencias en formato JSON
    if not isinstance(pertenencias, list):
        return jsonify({'error': 'Formato de datos incorrecto'}), 400
    try:
        PertenenciasServices.registrar_salida_pertenencias(pertenencias)
        return jsonify({'message': 'Salida de pertenencias registrada correctamente'}), 200
    
    except Exception as e:
        print(f"Error al registrar salida de pertenencias: {e}")
        return jsonify({'error': 'Ocurrió un error al procesar la solicitud'}), 500



# Ruta para mostrar la imagen de una pertenencia
@pertenencias_bp.route('/pertenencia/imagen/<filename>')
def mostrar_imagen_pertenencia(filename):
    try:
        return PertenenciasServices.mostrar_imagen_pertencia(filename)
    except Exception as e:
        print(f"Error al mostrar la imagen: {e}")
        return jsonify({'error': 'Ocurrió un error al mostrar la imagen'}), 500