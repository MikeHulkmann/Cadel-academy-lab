from flask import Blueprint, render_template, request, redirect, url_for, session
from utils.db import get_db_connection
from utils.middleware import get_security_level

bp = Blueprint('chat', __name__)

@bp.route('/chat', methods=['GET'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    search_query = request.args.get('q', '')
    search_results = []
    error = None
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    # --- Lógica de Búsqueda de Usuarios ---
    if search_query:
        if get_security_level() == 'vulnerable':
            # [VULNERABLE] SQL Injection en cláusula LIKE
            # Permite enumerar usuarios o extraer datos con UNION.
            # Payload ejemplo: ' UNION SELECT 1, @@version -- -
            query = f"SELECT id, username FROM users WHERE username LIKE '%{search_query}%' AND id != {user_id}"
            try:
                cursor.execute(query)
                search_results = cursor.fetchall()
            except Exception as e:
                error = f"Error SQL: {e}"
        else:
            # [SEGURO] Uso de parámetros para sanitizar la entrada
            query = "SELECT id, username FROM users WHERE username LIKE %s AND id != %s"
            cursor.execute(query, (f"%{search_query}%", user_id))
            search_results = cursor.fetchall()

    # --- Obtener Conversaciones Existentes ---
    cursor.execute("""
        SELECT DISTINCT u.id, u.username
        FROM users u
        JOIN private_messages pm ON u.id = pm.sender_id OR u.id = pm.receiver_id
        WHERE (pm.sender_id = %s OR pm.receiver_id = %s) AND u.id != %s
    """, (user_id, user_id, user_id))
    conversations = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('chat.html', conversations=conversations, search_results=search_results, search_query=search_query, error=error)


@bp.route('/chat/<int:other_user_id>', methods=['GET', 'POST'])
def conversation(other_user_id):
    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            cursor.execute(
                "INSERT INTO private_messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)",
                (user_id, other_user_id, message)
            )
            conn.commit()
        return redirect(url_for('chat.conversation', other_user_id=other_user_id))

    cursor.execute("""
        SELECT pm.*, u_sender.username as sender_username
        FROM private_messages pm
        JOIN users u_sender ON pm.sender_id = u_sender.id
        WHERE (pm.sender_id = %s AND pm.receiver_id = %s) OR (pm.sender_id = %s AND pm.receiver_id = %s)
        ORDER BY pm.created_at ASC
    """, (user_id, other_user_id, other_user_id, user_id))
    messages = cursor.fetchall()
    
    # Obtener información del otro usuario para mostrar su nombre en el chat
    cursor.execute("SELECT username FROM users WHERE id = %s", (other_user_id,))
    other_user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('conversation.html', messages=messages, other_user=other_user, other_user_id=other_user_id)