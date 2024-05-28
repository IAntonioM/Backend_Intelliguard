import sqlite3
class Usuario:
    def __init__(self, id_usuario, usuario, hash_contraseña, id_rol, rol):
        self.id_usuario = id_usuario
        self.usuario = usuario
        self.hash_contraseña = hash_contraseña
        self.id_rol = id_rol
        self.rol = rol
class BaseDatosUsuarios:
    def __init__(self, nombre_archivo):
        self.conexion = sqlite3.connect(nombre_archivo)
        self.cursor = self.conexion.cursor()
        self.crear_tabla_usuarios()
    def crear_tabla_usuarios(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                                usuario TEXT NOT NULL,
                                hash_contraseña TEXT NOT NULL,
                                id_rol INTEGER NOT NULL,
                                FOREIGN KEY (id_rol) REFERENCES rol_usuario(id)
                            )''')
        self.conexion.commit()
    def agregar_usuario(self, usuario, contraseña, idRol):
        self.cursor.execute("INSERT INTO usuarios (usuario, hash_contraseña, id_rol) VALUES (?, ?, ?)", (usuario, contraseña, idRol))
        self.conexion.commit()
    def consultar_usuario_por_usuario(self, usuario):
        self.cursor.execute("""
            SELECT u.id_usuario, u.usuario, u.hash_contraseña, u.id_rol, r.rol
            FROM usuarios u
            LEFT JOIN rol_usuario r ON u.id_rol = r.id
            WHERE u.usuario = ?
        """, (usuario,))
        resultado = self.cursor.fetchone()
        if resultado:
            id_usuario, usuario, hash_contraseña, id_rol, rol = resultado
            return Usuario(id_usuario, usuario, hash_contraseña, id_rol, rol)
        else:
            return None
    def eliminar_tabla_usuarios(nombre_archivo):
        conexion = sqlite3.connect(nombre_archivo)
        cursor = conexion.cursor()
        # Sentencia SQL para eliminar la tabla usuarios
        cursor.execute("DROP TABLE IF EXISTS usuarios")
        # Confirmar los cambios y cerrar la conexión
        conexion.commit()
        conexion.close()
# BaseDatosUsuarios.eliminar_tabla_usuarios("basededatos.db")