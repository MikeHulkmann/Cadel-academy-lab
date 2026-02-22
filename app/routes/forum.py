from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, jsonify
import os
from werkzeug.utils import secure_filename
from utils.db import get_db_connection
from utils.middleware import get_security_level

bp = Blueprint('forum', __name__)

@bp.route('/forum', methods=['GET', 'POST'])
def index():
    # Verificar si el usuario está logueado
    if 'user_id' not in session:
        return redirect(url_for('login.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author_id = session['user_id']
        file = request.files.get('file')
        
        filename = None
        filepath = None

        # Handle file upload
        if file and file.filename != '':
            filename = file.filename
            if get_security_level() == 'secure':
                # [SEGURO] Validación de extensión (Lista Blanca) y sanitización de nombre
                allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
                if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                    # In a real app, flash an error message
                    return "Error: Tipo de archivo no permitido", 400
                filename = secure_filename(filename)
            
            # [VULNERABLE] No se valida la extensión ni el contenido.
            # Permite subir archivos peligrosos como .html (XSS) o scripts (.php, .py) para RCE.
            
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            
            filepath_full = os.path.join(upload_folder, filename)
            file.save(filepath_full)
            filepath = os.path.join('uploads', filename) # Relative path for URL

        # A post must have content or a file
        if (title or content) or filename:
            cursor.execute(
                "INSERT INTO posts (title, content, author_id, filename, filepath) VALUES (%s, %s, %s, %s, %s)",
                (title, content, author_id, filename, filepath)
            )
            conn.commit()
        
        return redirect(url_for('forum.index'))

    # Obtener todos los posts ordenados por el más reciente
    cursor.execute("SELECT p.*, u.username FROM posts p JOIN users u ON p.author_id = u.id ORDER BY p.id DESC")
    posts = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('forum.html', posts=posts)

@bp.route('/forum/star/<int:post_id>', methods=['POST'])
def star_post(post_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    # Increment star count
    cursor.execute("UPDATE posts SET stars = stars + 1 WHERE id = %s", (post_id,))
    conn.commit()

    # Get the new count
    cursor.execute("SELECT stars FROM posts WHERE id = %s", (post_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return jsonify({'stars': result['stars']})
    else:
        return jsonify({'error': 'Post not found'}), 404