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

    def identificarObjeto(img_archivo):
        try:
            imagen = cv2.imread(img_archivo)
            ruta_modelo = os.path.join('models', 'best.pt') 
            modelo = YOLO(ruta_modelo) 
            resultados = modelo.predict(imagen, imgsz=640, conf=0.80)
            if resultados is not None and len(resultados) > 0 and len(resultados[0].boxes) > 0:
                etiquetas = [resultados[0].names[int(etiqueta)] for etiqueta in resultados[0].boxes.cls]
                etiquetas_unidas = ', '.join(etiquetas)
                return etiquetas_unidas
            else:
                print("No se encontraron objetos en la imagen.")
                return -1
        except Exception as error:
            print(f"Error en la detección de objetos: {str(error)}")
            return -1
        
        
    # def entrenar_modelo_objeto(ruta_train, ruta_val, ruta_modelo, epochs=150, batch_size=16):
    #     try:
    #         modelo = YOLO('yolov8n.pt')
    #         datos = {
    #             'train': ruta_train,
    #             'val': ruta_val
    #         }
    #         hyperparams = {
    #             'epochs': epochs,
    #             'batch_size': batch_size,
    #         }
    #         print("Comenzando el entrenamiento del modelo...")
    #         modelo.train(data=datos, **hyperparams)
    #         modelo.save(ruta_modelo)
    #         print(f"Modelo entrenado guardado en: {ruta_modelo}")
    #     except Exception as e:
    #         print(f"Error durante el entrenamiento del modelo YOLOv8: {str(e)}")
    # ruta_train = 'path/to/train'
    # ruta_val = 'path/to/val'
    # ruta_modelo = 'models/yolov8_best.pt'
    # entrenar_modelo_objeto(ruta_train, ruta_val, ruta_modelo)

