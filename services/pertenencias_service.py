import cv2
from utils.deteccion_objetos import DeteccionObjetos
from utils.comparar_pertenencia import ordenar_imagenes_por_similitud
from models.objeto import Objeto,BaseDatosObjetos
from models.registros_pertencia import RegistrosPertenencia,BaseDatosRegistrosPertenencia
from models.pertenencia import Pertenencia,BaseDatosPertenencia
from datetime import datetime
import os
from flask import  send_from_directory,current_app
import base64


class PertenenciasService:
    def __init__(self):
        # Aquí podrías inicializar cualquier cosa necesaria para tu servicio
        pass
            
            # if pertenencias == -1:
            #     return -1
            # else:
            #     for pertenencia in pertenencias:
            #         print(pertenencia.imagen_pertenencia)
            #     for registro in registrosPertenecia:
            #         print(registro.hora_entrada)
            #     return -1
            
    def registrar_nueva_pertenencia(img_file,idEstudiante,idObjeto):
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        estadoPertenencia=1
        # Crear la carpeta si no existe
        uploads_path = os.path.join('uploads', 'pertenencia')
        if not os.path.exists(uploads_path):
            os.makedirs(uploads_path)
        img_name=f"{idEstudiante}_{fecha_hora_actual}.jpg"
        # Guardar la imagen de la pertenencia en la carpeta 'uploads/pertenencia'
        img_path = os.path.join(uploads_path, img_name)
        # Leer el contenido del FileStorage como bytes
        imagen_bytes = img_file.read()
        with open(img_path, 'wb') as img_file:
            img_file.write(imagen_bytes)
        base_datos_pertenencia = BaseDatosPertenencia("basededatos.db")
        base_datos_registrosPertenencia = BaseDatosRegistrosPertenencia("basededatos.db")
        print(idObjeto)
        codigoPertenencia = base_datos_pertenencia.registrar_pertenencia(idObjeto, img_name, idEstudiante, estadoPertenencia, fecha_hora_actual)
        
        print("codigoPerte:")
        print(codigoPertenencia)
        if codigoPertenencia == -1:
            return -1
        else:
            resultado = base_datos_registrosPertenencia.registrar_registro(idEstudiante,idObjeto,estadoPertenencia,codigoPertenencia,fecha_hora_actual,img_name)
            if resultado == -1:
                return -1
            else:
                return resultado

    def registrar_entrada_pertenencia(img_file,idEstudiante,idObjeto,codigoPertenencia):
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  
        estadoPertenencia=1
        # Crear la carpeta si no existe
        uploads_path = os.path.join('uploads', 'pertenencia')
        if not os.path.exists(uploads_path):
            os.makedirs(uploads_path)
        img_name=f"{idEstudiante}_{fecha_hora_actual}.jpg"
        # Guardar la imagen de la pertenencia en la carpeta 'uploads/pertenencia'
        img_path = os.path.join(uploads_path, img_name)
        # Leer el contenido del FileStorage como bytes
        imagen_bytes = img_file.read()
        with open(img_path, 'wb') as img_file:
            img_file.write(imagen_bytes)
        base_datos_pertenencia = BaseDatosPertenencia("basededatos.db")
        base_datos_registrosPertenencia = BaseDatosRegistrosPertenencia("basededatos.db")
        resultado = base_datos_registrosPertenencia.registrar_registro(idEstudiante,idObjeto,estadoPertenencia,codigoPertenencia,fecha_hora_actual,img_name)
        if resultado == -1:
            return -1
        else:
            resultado = base_datos_pertenencia.actualizar_pertenencia_por_actividad(codigoPertenencia,estadoPertenencia,fecha_hora_actual)
            if resultado == -1:
                return -1
            else:
                return 1
        
    def consultar_pertenencia_estado_estudiante(idEstudiante,idEstado):
        base_datos_pertenencia = BaseDatosPertenencia("basededatos.db")
        pertenencias=base_datos_pertenencia.consultar_pertenencias_por_estado_estudiante(idEstado,idEstudiante)
        if pertenencias == []:
            return -1
        else:
            registros_dic=[]
            for p in pertenencias:
                    UPLOAD_FOLDER = 'uploads/pertenencia'
                    imagen_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, p.imagen_pertenencia)
                    with open(imagen_path, 'rb') as imagen_file:
                        imagen_base64 = base64.b64encode(imagen_file.read()).decode('utf-8')
                    pertenencia_dict = {
                        'codigo_pertenencia': p.codigo_pertenencia,
                        'tipo_objeto': p.tipo_objeto,
                        'nombre_objeto': p.objeto_text,
                        'hora_entrada': p.fecha_ultima_actividad,
                        'id_estado': p.id_ultimo_estado,
                        'nombre_estado': p.estado_text,
                        'imagen_pertenencia': f'data:image/jpeg;base64,{imagen_base64}',
                        'id_estudiante': p.id_estudiante
                    }
                    registros_dic.append(pertenencia_dict)
        return registros_dic



    def registrar_salida_pertenencia(codPertenciasIdEstado):
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Reemplazar los dos puntos con guiones bajos
        try:
            base_datos_pertenencia = BaseDatosPertenencia("basededatos.db")
            for pertenencia in codPertenciasIdEstado:
                codPertenencia=pertenencia.get('codPertenecia')
                estado=pertenencia.get('estado')
                if not codPertenencia or estado is None:
                    continue
                if not base_datos_pertenencia.cambiar_estado_pertenencias(codPertenencia,estado,fecha_hora_actual):
                        return False
                base_datos_registrosPertenencia = BaseDatosRegistrosPertenencia("basededatos.db")
                base_datos_registrosPertenencia.actualizar_hora_estado_registro(codPertenencia,estado,fecha_hora_actual)
            return True
        except Exception as e:
            print(f"Error al registrar salida de perteencia {e}")
            return False

    def consultar_pertencias_estudiante_busqueda(datosEstudainte,estadoRegistros,codigoPertenencia):
        try:
            base_datos_pertenencia = BaseDatosPertenencia("basededatos.db")
            pertenencias=base_datos_pertenencia.consultar_pertencias_estudiante_busqueda(datosEstudainte,estadoRegistros,codigoPertenencia)
            registros_dic=[]
            for p in pertenencias:
                    UPLOAD_FOLDER = 'uploads/pertenencia'
                    imagen_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, p.imagen_pertenencia)
                    with open(imagen_path, 'rb') as imagen_file:
                        imagen_base64 = base64.b64encode(imagen_file.read()).decode('utf-8')
                    pertenencia_dict = {
                        'codigo_pertenencia': p.codigo_pertenencia,
                        'tipo_objeto': p.tipo_objeto,
                        'nombre_objeto': p.objeto_text,
                        'hora_ultima_actividad': p.fecha_ultima_actividad,
                        'id_estado': p.id_ultimo_estado,
                        'nombre_estado': p.estado_text,
                        'imagen_pertenencia': f'data:image/jpeg;base64,{imagen_base64}',
                        'id_estudiante': p.id_estudiante,
                        'codigo_estudiante': p.codigo_estudiante,
                        'nombres_estudiante': p.nombres_estudiante,
                        'carrera_estudiante': p.carrera_estudiante,
                        'plan_estudiante': p.plan_estudiante
                    }
                    registros_dic.append(pertenencia_dict)
            return registros_dic
        except Exception as e:
            print(f"Error al registrar salida de perteencia {e}")
            return -1
        
    def consultar_registros_pertencia(datosEstudiante,estadoRegistros,codigoPertenencia):
        try:
            base_datos_registrosPertenencia = BaseDatosRegistrosPertenencia("basededatos.db")
            registros=base_datos_registrosPertenencia.consultar_registros_pertencia_busqueda(datosEstudiante,estadoRegistros,codigoPertenencia)
            registros_dic=[]
            for r in registros:
                    # Obtener la ruta completa de la imagen
                    UPLOAD_FOLDER = 'uploads/pertenencia'
                    imagen_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, r.imagen_pertenencia)
                    
                    # Leer la imagen y convertirla a base64
                    with open(imagen_path, 'rb') as imagen_file:
                        imagen_base64 = base64.b64encode(imagen_file.read()).decode('utf-8')
                    
                    # Construir el diccionario de pertenencia con la imagen en base64
                    pertenencia_dict = {
                        'id_registro': r.id_registro,
                        'id_estudiante': r.id_estudiante,
                        'id_objeto': r.id_objeto,
                        'hora_entrada': r.hora_entrada,
                        'imagen_pertenencia': f'data:image/jpeg;base64,{imagen_base64}',
                        'id_estado': r.id_estado,
                        'codigo_pertenencia': r.codigoPertenencia,
                        'hora_salida': r.hora_salida,
                        'estado': r.estado,
                        'nombre_objeto': r.nombre_objeto,
                        'nombres_estudiante': r.nombres_estudiante
                    }
                    registros_dic.append(pertenencia_dict)
            return registros_dic
        except Exception as e:
            print(f"Error al consultar datos de reporte {e}")
            return -1
    
    
