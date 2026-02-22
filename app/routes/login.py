from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, session
from utils.db import get_db_connection
from utils.middleware import get_security_level

bp = Blueprint('login', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        if get_security_level() == 'vulnerable':
            # [VULNERABLE] SQL Injection
            # La concatenación directa de strings permite al atacante manipular la consulta SQL.
            # Payload ejemplo: admin' OR '1'='1' -- -
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            try:
                print(f"[DEBUG SQL] Ejecutando: {query}") # Para ver en los logs
                cursor.execute(query)
                user = cursor.fetchone()
            except Exception as e:
                error = f"Error SQL: {e}"
                user = None
        else:
            # [SEGURO] Consultas Parametrizadas
            # El uso de marcadores de posición (%s) asegura que la base de datos trate
            # los inputs como datos literales y no como código ejecutable.
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
        cursor.close()
        conn.close()

        if user:
            # Login exitoso
            session['user_id'] = user['id'] # Guardar sesión en Flask
            session['username'] = user['username']
            resp = make_response(redirect(url_for('dashboard.dashboard')))
            
            # [AUDITORÍA] Gestión de Cookies
            if get_security_level() == 'vulnerable':
                # [VULNERABLE] Cookie accesible por JS (falta HttpOnly) y viaja en texto plano (falta Secure)
                resp.set_cookie('user_id', str(user['id']), httponly=False, secure=False, samesite='Lax')
            else:
                # [SEGURO] Cookie protegida contra XSS (HttpOnly) y MitM (Secure)
                resp.set_cookie('user_id', str(user['id']), httponly=True, secure=True, samesite='Strict')
            
            return resp
        elif not error:
            error = "Usuario o contraseña incorrectos"

    return render_template('login.html', error=error)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # En modo vulnerable, permitimos registros vacíos o débiles
        if not username or not password:
             if get_security_level() == 'secure':
                 error = "Todos los campos son obligatorios"
                 return render_template('register.html', error=error)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insertar usuario (Vulnerable a SQLi si no se valida, pero aquí usamos parametrizada por simplicidad en el registro)
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, 'user')", (username, password))
            conn.commit()
            return redirect(url_for('login.login'))
        except Exception as e:
            error = f"Error al registrar: {e}"
        finally:
            cursor.close()
            conn.close()
            
    return render_template('register.html', error=error)

@bp.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('user_id', '', expires=0)
    return resp