import cv2
import os
import imutils
import time
import numpy as np
import tempfile
from ultralytics import YOLO

class DeteccionObjetos:
    def __init__(self):
        # Aquí podrías inicializar cualquier cosa necesaria para tu servicio
        pass

    def identificarObjeto(img_path):
        try:
            # Cargar la imagen desde la ruta proporcionada
            frame = cv2.imread(img_path)

            # Realizar la predicción utilizando el modelo YOLO
            modelo_path = os.path.join('models', 'best.pt')  # Ruta al modelo YOLO
            modelo = YOLO(modelo_path)  # Crear una instancia del modelo YOLO
            results = modelo.predict(frame, imgsz=640, conf=0.80)  # Realizar la predicción

            # Verificar si se detectaron objetos
            if results is not None and len(results) > 0 and len(results[0].boxes) > 0:
                # Obtener las etiquetas de los objetos detectados
                etiquetas_objetos = [results[0].names[int(label)] for label in results[0].boxes.cls]

                # Obtener el texto resultante
                label = ', '.join(etiquetas_objetos)
                return label
            else:
                print("No se detectaron objetos en la imagen.")
                return -1
        except Exception as e:
            print(f"Error durante el proceso de detección de objetos: {str(e)}")
            return -1

