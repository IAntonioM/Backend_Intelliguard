from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.estudiantes_routes import estudiantes_bp
from routes.auth_routes import auth_bp
from routes.pertenencias_route import pertenencias_bp
from routes.registrosPertenencia_routes import registros_pertenencia_bp
from routes.objetos_routes import objetos_bp


from models.estudiante import BaseDatosEstudiantes
from models.usuario import BaseDatosUsuarios
from models.registros_pertencia import BaseDatosRegistrosPertenencia
from models.pertenencia import BaseDatosPertenencia



app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'clave_12323'
jwt = JWTManager(app)

base_datos_usuarios = BaseDatosUsuarios("basededatos.db")
base_datos_estudiantes = BaseDatosEstudiantes("basededatos.db")
base_datos_registrosPertenencia = BaseDatosRegistrosPertenencia("basededatos.db")
base_datos_pertenencia = BaseDatosPertenencia("basededatos.db")

@app.route('/')
def index():
    return 'Hola mundo'

app.register_blueprint(pertenencias_bp)
app.register_blueprint(estudiantes_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(registros_pertenencia_bp)
app.register_blueprint(objetos_bp)


if __name__ == '__main__':
    app.run(debug=True)

