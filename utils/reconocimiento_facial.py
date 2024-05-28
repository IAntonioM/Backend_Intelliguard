import cv2
import os
import imutils
import time
import numpy as np
import tempfile

class ReconocimientoFacial:
    def __init__(self):
        # Aquí podrías inicializar cualquier cosa necesaria para tu servicio
        pass

    def capturar_rostro(self,video_path, estudiante_path, codigoEstudiante):
        try:
            if not os.path.exists(estudiante_path):
                os.makedirs(estudiante_path)

            cap = cv2.VideoCapture(video_path)

            duracion_maxima = 10
            frames_por_segundo = cap.get(cv2.CAP_PROP_FPS)
            total_frames_a_capturar = int(frames_por_segundo * duracion_maxima)

            frames_capturados = 0

            rostro_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            while True:
                ret, frame = cap.read()
                # if not ret or frames_capturados >= total_frames_a_capturar:
                #     break
                if not ret :
                    break

                frame = imutils.resize(frame, width=640)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                auxFrame = frame.copy()
                rostros = rostro_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in rostros:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    recorte_rostro = auxFrame[y:y+h, x:x+w]
                    recorte_rostro_gris = cv2.cvtColor(recorte_rostro, cv2.COLOR_BGR2GRAY)
                    recorte_rostro_gris = cv2.resize(recorte_rostro_gris, (150, 150), interpolation=cv2.INTER_CUBIC)
                    img_rostro = f'{codigoEstudiante}_{int(time.time())}.jpg'
                    cv2.imwrite(os.path.join(estudiante_path, img_rostro), recorte_rostro_gris)
                # frames_capturados += 1

            cap.release()
            cv2.destroyAllWindows()
            print("Proceso de registro completado.")
        except Exception as e:
            print(f"Error durante el proceso de registro: {str(e)}")
        


    def entrenar_modelo(self):
            ruta_imgs_path = os.path.join('uploads', 'estudiante')
            modelo_path = os.path.join('models', 'modelFisherFace.xml')
            List = os.listdir(ruta_imgs_path)
            print('Lista de personas: ', List)

            labels = []
            datoRostro = []
            label = 0

            # Pasa las imagenes seleccionadas con su respectiva carpeta
            for nombreDir in List:
                carpeta_persona = os.path.join(ruta_imgs_path, nombreDir)
                print('Leyendo las imágenes en la carpeta:', nombreDir)
                label = int(nombreDir)  # Usar el nombre de la carpeta como ID

                # Pasa todas las imágenes dentro de la carpeta
                for nombre_archivo in os.listdir(carpeta_persona):
                    print('Rostros: ', nombre_archivo)
                    img_path = os.path.join(carpeta_persona, nombre_archivo)
                    labels.append(label)
                    img = cv2.imread(img_path, 0)  # Lee la imagen en escala de grises
                    datoRostro.append(img)

            # Especificacion del modelo
            reconocimiento_facial = cv2.face.FisherFaceRecognizer_create()
            # Entrenando...
            print("Entrenando...")
            reconocimiento_facial.train(datoRostro, np.array(labels))

            # Modelo generado
            reconocimiento_facial.write(modelo_path)
            print("Modelo almacenado en", modelo_path)

    def reconocimiento_facial(img_file):
        reconocimiento_facial = cv2.face.FisherFaceRecognizer_create()
        reconocimiento_facial.read(os.path.join('models', 'modelFisherFace.xml'))
        # Guardar imagen temporalmente
        imagen = cv2.imdecode(np.frombuffer(img_file.read(), np.uint8), cv2.IMREAD_COLOR)
        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        # Detectar rostros
        clasificacion_facial = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        rostros = clasificacion_facial.detectMultiScale(gray, 1.3, 5)
        # Verificar si se detectaron rostros
        if len(rostros) == 0:
            return -1, 0  # Devolver un código de error y un porcentaje de similitud de 0
        # Procesar cada rostro detectado
        for (x, y, w, h) in rostros:
            rostro = gray[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            result_id, similitud = reconocimiento_facial.predict(rostro)
            if similitud < 500:
                porcentaje_similitud = 100 - int(similitud / 5)
                return result_id, porcentaje_similitud
            else:
                return -1, 0  # Devolver un código de error y un porcentaje de similitud de 0 si la similitud es alta

        
