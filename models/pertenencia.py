import sqlite3
from datetime import datetime

class Pertenencia:
    def __init__(self, id_pertenencia, id_estudiante, id_objeto, id_estado, estado, fecha, imagen_pertenencia,nombre_objeto,nombres_estudiante):
        self.id_pertenencia = id_pertenencia
        self.id_estudiante = id_estudiante
        self.id_objeto = id_objeto
        self.id_estado = id_estado
        self.estado = estado
        self.fecha = fecha
        self.imagen_pertenencia = imagen_pertenencia
        self.nombre_objeto = nombre_objeto  # Nuevo atributo para almacenar el nombre del objeto
        self.nombres_estudiante = nombres_estudiante  # Nuevo atributo para almacenar el nombre del objeto


class BaseDatosPertenencias:
    def __init__(self, nombre_archivo):
        self.conexion = sqlite3.connect(nombre_archivo)
        self.cursor = self.conexion.cursor()
        self.crear_tabla_pertenencias()

    def crear_tabla_pertenencias(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS registro_pertenencias (
            idPertenencia INTEGER PRIMARY KEY AUTOINCREMENT,
            idEstudiante INTEGER,
            idObjeto INTEGER,
            idEstado INTEGER,
            Estado TEXT,
            Fecha DATETIME,
            imagenPertenencia TEXT,
            FOREIGN KEY (idEstudiante) REFERENCES estudiantes(idEstudiante),
            FOREIGN KEY (idObjeto) REFERENCES objetos(idObjeto),
            FOREIGN KEY (idEstado) REFERENCES estado_pertenencias(id)
        )''')
        self.conexion.commit()

    def guardar_pertenencia(self, id_estudiante, id_objeto, idEstado, fecha, imagen_pertenencia):
        try:
            self.cursor.execute('''INSERT INTO registro_pertenencias 
                                   (idEstudiante, idObjeto, idEstado, Fecha, imagenPertenencia) 
                                   VALUES (?, ?, ?, ?, ?)''',
                                (id_estudiante, id_objeto, idEstado, fecha, imagen_pertenencia))
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"Error al guardar la pertenencia: {e}")
            self.conexion.rollback()
            return -1
        return 1
    
    def consultar_pertencia_por_idEstudiante_fecha(self, idEstudiante, idEstado, fecha_actual):
        query = """
        SELECT rp.*, ep.estado AS Estado, o.Nombre AS nombreObjeto, e.Nombres AS nombreEstudiante
        FROM registro_pertenencias rp
        JOIN objetos o ON rp.idObjeto = o.idObjeto
        JOIN estudiantes e ON rp.idEstudiante = e.idEstudiante
        JOIN estado_pertenencias ep ON rp.idEstado = ep.id
        WHERE rp.idEstudiante = ? AND rp.idEstado = ? AND substr(rp.Fecha, 1, 10) = ?
        """
        self.cursor.execute(query, (idEstudiante, idEstado, fecha_actual))
        resultados = self.cursor.fetchall()
        pertenencias = []

        for resultado in resultados:
            pertenencia = Pertenencia(
                id_pertenencia=resultado[0],
                id_estudiante=resultado[1],
                id_objeto=resultado[2],
                fecha=resultado[3],
                imagen_pertenencia=resultado[4],
                id_estado=resultado[5],
                estado=resultado[6],
                nombre_objeto=resultado[7],
                nombres_estudiante=resultado[8]
            )
            pertenencias.append(pertenencia)

        return pertenencias
    
    def consultar_pertenencias_por_busqueda(self, busqueda):
        script_sql = """
            SELECT rp.*, ep.estado AS Estado , o.Nombre AS nombreObjeto, e.Nombres AS nombreEstudiante
            FROM registro_pertenencias rp
            JOIN objetos o ON rp.idObjeto = o.idObjeto
            JOIN estudiantes e ON rp.idEstudiante = e.idEstudiante
            JOIN estado_pertenencias ep ON rp.idEstado = ep.id
            WHERE e.Nombres LIKE ? OR e.codigoEstudiante LIKE ?;
        """
        self.cursor.execute(script_sql, (f"%{busqueda}%", f"%{busqueda}%"))
        resultados = self.cursor.fetchall()
        pertenencias = []
        for resultado in resultados:
            pertenencia = Pertenencia(
                id_pertenencia=resultado[0],
                id_estudiante=resultado[1],
                id_objeto=resultado[2],
                fecha=resultado[3],
                imagen_pertenencia=resultado[4],
                id_estado=resultado[5],
                estado=resultado[6],
                nombre_objeto=resultado[7],
                nombres_estudiante=resultado[8]
            )
            pertenencias.append(pertenencia)
        return pertenencias
    
    # Método en el modelo para cambiar el estado de pertenencias
    def cambiar_estado_pertenencias(self, id_pertenencia, idEstado):
        try:
            # Actualizar el estado de la pertenencia en la base de datos
            self.cursor.execute('''UPDATE registro_pertenencias 
                                SET idEstado = ? 
                                WHERE idPertenencia = ?''',
                                (idEstado, id_pertenencia))
            self.conexion.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al cambiar el estado de la pertenencia: {e}")
            self.conexion.rollback()
            return False
        
    def borrar_todas_las_pertenencias(self):
        self.cursor.execute("DELETE FROM registro_pertenencias")
        self.conexion.commit()

