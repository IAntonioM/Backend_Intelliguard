
from services.pertenencias_service import PertenenciasService
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, Blueprint, jsonify, request, send_from_directory
import os
from flask import current_app, send_from_directory
import base64
from utils.role_decorador import role_required
from openpyxl import Workbook
from io import BytesIO
from flask import send_file
import os
from flask import  send_from_directory,current_app
import base64
import numpy as np
from models.registros_pertencia import RegistrosPertenencia,BaseDatosRegistrosPertenencia

#from models.registros_pertencia import BaseDatosRegistrosPertenencia


pertenencias_bp = Blueprint('pertenencias', __name__)


# @pertenencias_bp.route('/pertenencia/consultar-objeto-pertenencia', methods=['POST'])
# # @jwt_required()
# # @role_required('Personal')
# def consultar_objeto_pertenencia():
#     try:
#         file = request.files['file']
#         if not file:
#             return jsonify({'error': 'El archivo es requerido'}), 400

#         idEstudiante = request.form.get('idEstudiante')
#         if not idEstudiante:
#             return jsonify({'error': 'El código del estudiante es requerido'}), 400

#         UPLOAD_FOLDER = 'uploads/pertenencia'
        
#         pertenencias, objeto, imagenRecortada = PertenenciasService.identificar_objeto_pertenencia(file, idEstudiante)

#         if pertenencias == "no object":
#             return jsonify({'error': 'no_object'}), 404

#         if imagenRecortada is not None:
#             _, buffer = cv2.imencode('.jpg', imagenRecortada)
#             imagen_recortada_base64 = base64.b64encode(buffer).decode('utf-8')
#         else:
#             return jsonify({'error': 'Error al procesar la imagen recortada'}), 500
        
#         if pertenencias == "no pertenencia":
#             return jsonify({
#                 'nombreObjeto': objeto.nombre,
#                 'idObjeto': objeto.id_objeto,
#                 'imagenRecortada': f'data:image/jpeg;base64,{imagen_recortada_base64}',
#                 'estado': "sin_registros"
#             }), 200

#         if objeto:
#             return jsonify({
#                 'nombreObjeto': objeto.nombre,
#                 'idObjeto': objeto.id_objeto,
#                 'estado': "coincidencias",
#                 'imagenRecortada': f'data:image/jpeg;base64,{imagen_recortada_base64}',
#                 'pertenencias_coincidencia': pertenencias
#             }), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    

@pertenencias_bp.route('/pertenencia/nueva-pertenencia', methods=['POST'])
@jwt_required()
@role_required('Personal')
def nueva_pertenecia():
    file = request.files['file']
    if not file:
        return jsonify({'error': 'El archivo es requerido'}), 400
    idEstudiante = request.form.get('idEstudiante')
    idObjeto = request.form.get('idObjeto')
    if not idEstudiante:
        return jsonify({'error': 'El id del estudiante es requerido'}), 400
    
    try:
        pertenencias = PertenenciasService.registrar_nueva_pertenencia(file,idEstudiante,idObjeto)
        if pertenencias == -1:
            return jsonify({'error': 'Error al registrar Pertenencia'}), 404
        else:
            return jsonify({'msg':'pertenencia registrada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@pertenencias_bp.route('/pertenencia/registrar-ingreso-pertenencia', methods=['POST'])
@jwt_required()
@role_required('Personal')
def ingreso_pertenecia():
    file = request.files['file']
    if not file:
        return jsonify({'error': 'El archivo es requerido'}), 400
    idEstudiante = request.form.get('idEstudiante')
    idObjeto = request.form.get('idObjeto')
    if not idEstudiante:
        return jsonify({'error': 'El id del estudiante es requerido'}), 400
    
    codigoPertenencia = request.form.get('codigoPertenencia')
    if not codigoPertenencia:
        return jsonify({'error': 'El codigoPertenencia es requerido'}), 400
    
    try:
        pertenencias = PertenenciasService.registrar_entrada_pertenencia(file,idEstudiante,idObjeto,codigoPertenencia)
        if pertenencias == -1:
            return jsonify({'error': 'Error al registrar ingreso Pertenencia'}), 404
        else:
            return jsonify({'msg':'ingreso de pertencia registrada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@pertenencias_bp.route('/pertenencia/consultar-pertenencia-estado-estudiante', methods=['POST'])
@jwt_required()
@role_required('Personal')
def consulta_registro_estado_estudiante():
    idEstudiante = request.form.get('idEstudiante')
    idEstado = request.form.get('idEstado')
    if not idEstudiante:
        return jsonify({'error': 'El id del estudiante es requerido'}), 400
    print("consulta")
    try:
        pertenencias = PertenenciasService.consultar_pertenencia_estado_estudiante(idEstudiante,idEstado)
        if pertenencias == -1:
            return jsonify({'error': 'Error al registrar Pertenencia'}), 404
        else:
            return jsonify({'pertenencias':pertenencias}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@pertenencias_bp.route('/pertenencia/registrar-salida-pertenencia', methods=['POST'])
@jwt_required()
@role_required('Personal')
def salida_pertenecia():
    data = request.get_json()
    if not isinstance(data,dict):
        return jsonify({'error': 'Formato de datos incorrecto'}), 400
    
    codPertenciasIdEstado=data.get('codPertenciaIdEstado')
    if not codPertenciasIdEstado or not isinstance(codPertenciasIdEstado,list):
        return jsonify({'error': 'Formato de datos incorrecto'}), 400
    
    try:
        PertenenciasService.registrar_salida_pertenencia(codPertenciasIdEstado)
        return jsonify({'msg':'pertenencia registrada exitosamente'}), 200
    except Exception as e:
        print('Error al registrar pertencias')
        return jsonify({'error': str(e)}), 500


@pertenencias_bp.route('/pertenencia/consultar-pertenencias-estudiante-busqueda', methods=['POST'])
@jwt_required()
@role_required('Personal')
def consulta_pertenencias_estudiante_busqueda():
    datosEstudiante = request.form.get('datosEstudiante', "")
    estadoRegistros = request.form.get('estadoRegistros', "")
    codigoPertenencia = request.form.get('codigoPertenencia', "")
    print("consulta")
    try:
        pertenencias = PertenenciasService.consultar_pertencias_estudiante_busqueda(datosEstudiante,estadoRegistros,codigoPertenencia)
        if pertenencias == -1:
            return jsonify({'error': 'Error al consultar Datos Pertenencia'}), 404
        else:
            return jsonify({'pertenencias':pertenencias}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pertenencias_bp.route('/pertenencia/consulta-reporte', methods=['POST'])
@jwt_required()
@role_required('Administrador')
def consulta_reporte():
    datosEstudiante = request.form.get('datosEstudiante')
    estadoRegistros = request.form.get('estadoRegistros')
    codigoPertenencia = request.form.get('codigoPertenencia')
    print("consulta")
    try:
        pertenencias = PertenenciasService.consultar_pertencias_estudiante_busqueda(datosEstudiante,estadoRegistros,codigoPertenencia)
        registros = PertenenciasService.consultar_registros_pertencia(datosEstudiante,estadoRegistros,codigoPertenencia)
        if pertenencias == -1 or registros == -1:
            return jsonify({'error': 'Error al consultar Datos de reporte'}), 404
        else:
            return jsonify({'pertenencias':pertenencias, 'registros':registros}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pertenencias_bp.route('/pertenencia/generar-excel', methods=['GET'])
def generar_excel():
    datosEstudiante = ""
    estadoPertenencia = ""
    codigoPertenencia = ""
    base_datos_registrosPertenencia = BaseDatosRegistrosPertenencia("basededatos.db")
    pertenencias = base_datos_registrosPertenencia.consultar_registros_pertencia_busqueda(datosEstudiante, estadoPertenencia, codigoPertenencia)
    
    # Crear un archivo Excel en memoria
    wb = Workbook()
    ws = wb.active
    ws.title = "Pertenencias"
    headers = ['ID Registro', 'Estado', 'Hora Entrada', 'Hora Salida', 'Cod Estudiante', 'Nombres Estudiante', 'Código Pertenencia', 'Nombre Objeto']
    ws.append(headers)
    
    if pertenencias and isinstance(pertenencias, list):
        for pertenencia in pertenencias:
            ws.append([
                pertenencia.id_registro,
                pertenencia.estado,
                pertenencia.hora_entrada,
                pertenencia.hora_salida,
                pertenencia.id_estudiante,
                pertenencia.nombres_estudiante,
                pertenencia.codigoPertenencia,
                pertenencia.nombre_objeto
            ])
    
    excel_buffer = BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)
    return send_file(
        excel_buffer,
        as_attachment=True,
        download_name="Pertenencias.xlsx",
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    



# @pertenencias_bp.route('/pertenencia/consultar-objeto-pertenencia', methods=['POST'])
# @jwt_required()
# @role_required('Personal')
# def consultar_objeto_pertenencia():
#     idEstudiante = request.form.get('idEstudiante')
#     file = request.files['file']
#     UPLOAD_FOLDER = 'uploads/pertenencia'
#     # Validar que el código del estudiante no esté vacío
#     if not idEstudiante:
#         return jsonify({'error': 'El código del estudiante es requerido'}), 400

#     try:
#         pertenencias = PertenenciasServices.consultar_pertencia_por_idEstudiante(idEstudiante, )
#         if pertenencias == -1:
#             return jsonify({'error': 'No hay pertenencias registradas del estudiante'}), 404
#         else:
#             # Formatear la respuesta JSON con la lista de pertenencias
#             pertenencias_json = []
#             for pertenencia in pertenencias:
#                 # Obtener la ruta completa de la imagen
#                 imagen_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, pertenencia.imagen_pertenencia)

#                 # Codificar la imagen en base64
#                 with open(imagen_path, 'rb') as imagen_file:
#                     imagen_base64 = base64.b64encode(imagen_file.read()).decode('utf-8')

#                 pertenencias_json.append({
#                     'idPertenencia': pertenencia.id_pertenencia,
#                     'idEstudiante': pertenencia.id_estudiante,
#                     'idObjeto': pertenencia.id_objeto,
#                     'Fecha': pertenencia.fecha,
#                     'nombreObjeto' : pertenencia.nombre_objeto,
#                     'nombresEstudiante' : pertenencia.nombres_estudiante,
#                     'ImagenPertenencia': f'data:image/jpeg;base64,{imagen_base64}',
#                 })

#             return jsonify({'pertenencias': pertenencias_json}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    

# @pertenencias_bp.route('/pertenencia/consultar-pertenencia-busqueda', methods=['POST'])
# @jwt_required()
# @role_required('Personal','Administrador')
# def consultar_pertenencia_por_busqueda():
#     busqueda = request.form.get('busqueda')
#     UPLOAD_FOLDER = 'uploads/pertenencia'
#     if not busqueda:
#         busqueda=''
#     try:
#         pertenencias = PertenenciasServices.consultar_pertencia_por_busqueda(busqueda)
#         if pertenencias == -1:
#             return jsonify({'error': 'Sin restulados de Busqueda ...'}), 404
#         else:
#             pertenencias_json = []
#             for pertenencia in pertenencias:
#                 imagen_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, pertenencia.imagen_pertenencia)
#                 with open(imagen_path, 'rb') as imagen_file:
#                     imagen_base64 = base64.b64encode(imagen_file.read()).decode('utf-8')
#                 pertenencias_json.append({
#                     'idPertenencia': pertenencia.id_pertenencia,
#                     'idEstudiante': pertenencia.id_estudiante,
#                     'idObjeto': pertenencia.id_objeto,
#                     'idEstado': pertenencia.id_estado,
#                     'Estado': pertenencia.estado,
#                     'Fecha': pertenencia.fecha,
#                     'nombreObjeto' : pertenencia.nombre_objeto,
#                     'nombresEstudiante' : pertenencia.nombres_estudiante,
#                     'ImagenPertenencia': f'data:image/jpeg;base64,{imagen_base64}',
#                 })
#             return jsonify({'pertenencias': pertenencias_json}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500





# #Ruta para mostrar la imagen de una pertenencia
# @pertenencias_bp.route('/pertenencia/imagen/<filename>')
# def mostrar_imagen_pertenencia(filename):
#     try:
#         return PertenenciasServices.mostrar_imagen_pertencia(filename)
#     except Exception as e:
#         print(f"Error al mostrar la imagen: {e}")
#         return jsonify({'error': 'Ocurrió un error al mostrar la imagen'}), 500