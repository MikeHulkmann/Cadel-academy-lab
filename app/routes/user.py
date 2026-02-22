from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.db import get_db_connection
from utils.middleware import get_security_level

bp = Blueprint('user', __name__)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_profile':
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            address = request.form.get('address')
            city = request.form.get('city')
            website = request.form.get('website')
            bio = request.form.get('bio')

            # [NOTA DE AUDITORÍA]
            # Los datos se guardan tal cual en la base de datos.
            # La vulnerabilidad XSS Stored ocurre en el momento de la visualización (renderizado), no en el guardado.
            cursor.execute("""
                UPDATE users 
                SET full_name=%s, email=%s, phone=%s, address=%s, city=%s, website=%s, bio=%s
                WHERE id=%s
            """, (full_name, email, phone, address, city, website, bio, user_id))
            conn.commit()
            flash("Perfil actualizado correctamente.")
        
        elif action == 'change_password':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            
            # Verificar contraseña actual
            cursor.execute("SELECT password FROM users WHERE id=%s", (user_id,))
            user = cursor.fetchone()
            
            if user and user['password'] == current_password:
                cursor.execute("UPDATE users SET password=%s WHERE id=%s", (new_password, user_id))
                conn.commit()
                flash("Contraseña cambiada correctamente.")
            else:
                flash("La contraseña actual es incorrecta.")

        return redirect(url_for('user.profile'))

    # Obtener datos del usuario
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return render_template('user.html', user=user)