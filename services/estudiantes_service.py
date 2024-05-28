import time
import os
import cv2
from matplotlib import pyplot
import imutils
import numpy as np
import tempfile
import subprocess
from utils.reconocimiento_facial import ReconocimientoFacial
from models.estudiante import Estudiante,BaseDatosEstudiantes

class EstudiantesService:
    def __init__(self):
        # Aquí podrías inicializar cualquier cosa necesaria para tu servicio
        pass


    def identificar_estudiante(self, img_file):
        print("identificar_estudiante")
        codigo_Estudiante, porcentaje_similitud = ReconocimientoFacial.reconocimiento_facial(img_file)
        print("identificar_estudiante2")
        if codigo_Estudiante == -1:
            return -1, 0
        else:
            base_datos_estudiantes = BaseDatosEstudiantes("basededatos.db")
            resultado = base_datos_estudiantes.consultar_estudiante_por_codigo(codigo_Estudiante)
            return resultado, porcentaje_similitud
    





    def registrar_estudiante(self, video_file, nombreCompleto, codigoEstudiante):
        video_path = os.path.join('uploads','videos',codigoEstudiante)
        estudiante_path = os.path.join('uploads', 'estudiante', codigoEstudiante)
        
        if not os.path.exists(video_path):
            os.makedirs(video_path)
        video_path = os.path.join(video_path,'video.webm')
        with open(video_path, 'wb') as webm_file:
            webm_file.write(video_file.read())
        estudiante = Estudiante(None, nombreCompleto, codigoEstudiante)
        base_datos_estudiantes = BaseDatosEstudiantes("basededatos.db")
        base_datos_estudiantes.guardar_estudiante(estudiante)
        ReconocimientoFacial.capturar_rostro(self,video_path,estudiante_path,codigoEstudiante)
        ReconocimientoFacial.entrenar_modelo(self)





    def entrenar_modelo(self):
        base_datos_estudiantes = BaseDatosEstudiantes("basededatos.db")
        base_datos_estudiantes.borrar_todos_los_estudiantes()

    