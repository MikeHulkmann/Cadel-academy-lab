import os
from flask import Flask, render_template, g, Response
from utils.db import init_db

app = Flask(__name__)

# Configuración básica
app.config['SECRET_KEY'] = 'clave_secreta_para_demos'
SECURITY_LEVEL = os.getenv('SECURITY_LEVEL', 'vulnerable')
app.config['SECURITY_LEVEL'] = SECURITY_LEVEL # Establecer en la config
# Inicializar rutas
from routes import login, search, posts, dashboard, blog, forum, chat, help, user
app.register_blueprint(login.bp)
app.register_blueprint(search.bp)
app.register_blueprint(posts.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(blog.bp)
app.register_blueprint(forum.bp)
app.register_blueprint(chat.bp)
app.register_blueprint(help.bp)
app.register_blueprint(user.bp)

# Importar el middleware
from utils.middleware import load_security_level, get_security_level

# Registrar el middleware para que se ejecute antes de procesar cualquier ruta.
# Esto asegura que 'g.security_level' esté disponible en toda la aplicación.
@app.before_request
def before_request():
    load_security_level()

# Inyectar la variable security_level en todas las plantillas HTML automáticamente.
# Evita tener que pasar 'security_level=...' manualmente en cada render_template().
@app.context_processor
def inject_security_level():
    return dict(security_level=get_security_level())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/robots.txt')
def robots():
    # Exponemos rutas sensibles para que herramientas de reconocimiento las encuentren
    content = "User-agent: *\nDisallow: /secret_config\n"
    return Response(content, mimetype='text/plain')

@app.route('/secret_config')
def secret_config():
    # Simula un archivo de configuración expuesto
    content = "DB_HOST=localhost\nDB_USER=root\nDB_PASS=root\nAPI_KEY=12345-ABCDE"
    return Response(content, mimetype='text/plain')

if __name__ == '__main__':
    # Inicializamos la BD antes de arrancar el servidor
    init_db()
    app.run(host='0.0.0.0', port=5000)