from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from routes.objetos_routes import objetos_bp
from routes.estudiantes_routes import estudiantes_bp
from routes.auth_routes import auth_bp
from routes.pertenencias_route import pertenencias_bp

from models.estudiante import BaseDatosEstudiantes
from models.usuario import BaseDatosUsuarios
from models.pertenencia import BaseDatosPertenencias


app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'clave_12323'
jwt = JWTManager(app)

base_datos_usuarios = BaseDatosUsuarios("basededatos.db")
base_datos_estudiantes = BaseDatosEstudiantes("basededatos.db")
base_datos_pertenencias = BaseDatosPertenencias("basededatos.db")

@app.route('/')
def index():
    return 'Hola mundo'

app.register_blueprint(objetos_bp)
app.register_blueprint(estudiantes_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(pertenencias_bp)


if __name__ == '__main__':
    app.run(debug=True)

