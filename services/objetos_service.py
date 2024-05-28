import time
import os
import cv2
from matplotlib import pyplot
import imutils
import numpy as np
import tempfile
import subprocess
from utils.deteccion_objetos import DeteccionObjetos
from models.objeto import Objeto,BaseDatosObjetos
from models.pertenencia import Pertenencia,BaseDatosPertenencias
from datetime import datetime




class ObjetosServices:
    def __init__(self):
        # Aquí podrías inicializar cualquier cosa necesaria para tu servicio
        pass

    def identificar_objeto(img_file):
        posicion=DeteccionObjetos.identificarObjeto(img_file)
        if posicion == -1:
            return -1
        else:
            base_datos_objetos = BaseDatosObjetos("basededatos.db")
            resultado = base_datos_objetos.consultar_objeto_por_id(posicion)
            return resultado
        

