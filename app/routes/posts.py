from flask import Blueprint, render_template, request, redirect, url_for
from utils.db import get_db_connection

bp = Blueprint('posts', __name__)

@bp.route('/post/<int:id>', methods=['GET', 'POST'])
def view_post(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Lógica para guardar nuevo comentario
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            # Guardamos el comentario en la BD.
            # Nota: La vulnerabilidad XSS Stored ocurre al MOSTRAR este dato en el HTML,
            # no necesariamente al guardarlo (aunque sanitizar al guardar es buena práctica).
            # Aquí confiamos en la mitigación de salida (Output Encoding) del template en modo seguro.
            cursor.execute("INSERT INTO comments (post_id, content) VALUES (%s, %s)", (id, content))
            conn.commit()
        return redirect(url_for('posts.view_post', id=id))

    # Obtener la noticia
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()

    # Obtener los comentarios asociados
    cursor.execute("SELECT * FROM comments WHERE post_id = %s ORDER BY id DESC", (id,))
    comments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('post.html', post=post, comments=comments)