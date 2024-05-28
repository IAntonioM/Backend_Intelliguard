
import os
from models.pertenencia import BaseDatosPertenencias
from datetime import datetime
from flask import  send_from_directory,current_app


class PertenenciasServices:
    def __init__(self):
        # Aquí podrías inicializar cualquier cosa necesaria para tu servicio
        pass


    def registrar_pertenencia(idEstudiante, id_objeto, imagen_pertenencia):
        base_datos_pertenencias = BaseDatosPertenencias("basededatos.db")
        estado = 1
        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Reemplazar los dos puntos con guiones bajos

        # Crear la carpeta si no existe
        uploads_path = os.path.join('uploads', 'pertenencia')
        if not os.path.exists(uploads_path):
            os.makedirs(uploads_path)
        img_name=f"{idEstudiante}_{fecha_actual}.jpg"
        # Guardar la imagen de la pertenencia en la carpeta 'uploads/pertenencia'
        img_path = os.path.join(uploads_path, img_name)
        
        # Leer el contenido del FileStorage como bytes
        imagen_bytes = imagen_pertenencia.read()

        with open(img_path, 'wb') as img_file:
            img_file.write(imagen_bytes)

        base_datos_pertenencias.guardar_pertenencia(idEstudiante, id_objeto, estado, fecha_actual, img_name)

    def registrar_salida_pertenencias(pertenecias):
        try:
            base_datos_pertenencias = BaseDatosPertenencias("basededatos.db")
            for pertenencia in pertenecias:
                # Actualizar el estado de la pertenencia en la base de datos
                if not base_datos_pertenencias.cambiar_estado_pertenencias(pertenencia, 2):
                    return False
            return True
        except Exception as e:
            print(f"Error al registrar salida de pertenencias: {e}")
            return False

    def consultar_pertencia_por_idEstudiante(idEstudiante,idEstado):
        # Obtener la fecha actual en formato YYYY-MM-DD
        fecha_actual = datetime.now().strftime("%Y-%m-%d")  
        base_datos_pertenencias = BaseDatosPertenencias("basededatos.db")
        # Consultar pertenencias por código de estudiante y fecha actual
        pertenencias = base_datos_pertenencias.consultar_pertencia_por_idEstudiante_fecha(idEstudiante, idEstado, fecha_actual)
        
        if not pertenencias:
            return -1
        else:
            return pertenencias
    
    def consultar_pertencia_por_busqueda(busqueda):
        base_datos_pertenencias = BaseDatosPertenencias("basededatos.db")
        # Consultar pertenencias por código de estudiante y fecha actual
        pertenencias = base_datos_pertenencias.consultar_pertenencias_por_busqueda(busqueda)
        
        if not pertenencias:
            return -1
        else:
            return pertenencias

    def mostrar_imagen_pertencia(filename):
        try:
            # Obtener la ruta completa del directorio de subida
            UPLOAD_FOLDER = 'uploads/pertenencia'
            directory = os.path.join(current_app.root_path, UPLOAD_FOLDER)
            # Devolver el archivo de imagen desde el directorio de subida
            return send_from_directory(directory, filename)
        except Exception as e:
            print(f"Error al mostrar la imagen: {e}")
            return None
