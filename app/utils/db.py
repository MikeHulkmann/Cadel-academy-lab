import mysql.connector
import time
import os

def get_db_connection():
    """
    Establece conexión con la base de datos MySQL.
    Incluye lógica de reintento (backoff) para esperar a que el contenedor de BD esté listo al iniciar Docker.
    """
    # Reintentamos la conexión porque a veces la BD tarda en levantar en Docker
    retries = 10
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host='db',
                user='root',
                password=os.environ.get('MYSQL_ROOT_PASSWORD', 'root'),
                database=os.environ.get('MYSQL_DATABASE', 'cadel_db')
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Esperando a la base de datos... ({retries} intentos restantes)")
            time.sleep(5)
            retries -= 1
    raise Exception("No se pudo conectar a la base de datos")

def init_db():
    """
    Inicializa la estructura de la base de datos y carga datos de prueba.
    Diseñado para ser idempotente (no duplica datos si se ejecuta varias veces o hay concurrencia).
    """
    try:
        conn = get_db_connection()
        # buffered=True es crítico para evitar errores de 'Unread result found' cuando hay múltiples consultas pendientes
        cursor = conn.cursor(buffered=True)
        
        # Crear tabla de usuarios si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(50) NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            full_name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            address VARCHAR(255),
            city VARCHAR(100),
            website VARCHAR(255),
            bio TEXT
            )
        """)
        
        # Crear tabla de posts (Foro de la Academia)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100),
            content TEXT,
            author_id INT,
            filename VARCHAR(255),
            filepath VARCHAR(255),
            stars INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Crear tabla de comentarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                post_id INT,
                content TEXT,
                author_id INT,
                FOREIGN KEY (post_id) REFERENCES posts(id)
            )
        """)
        
        # Crear tabla de mensajes privados (Chat 1-a-1)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS private_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender_id INT,
            receiver_id INT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
            )
        """)

        # Crear tabla de archivos (Uploads)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255),
                filepath VARCHAR(255),
                uploaded_by INT
            )
        """)
        
        conn.commit()

        # Insertar datos de prueba
        # Usamos INSERT IGNORE para evitar errores si ya existen (race condition)
        
        # 1. Usuarios
        users = [
            (1, 'admin', 'admin123', 'admin', 'Administrador del Sistema', 'admin@cadel.academy', 'Madrid', 'Soy el administrador de la plataforma.'),
            (2, 'profesor', 'profesor123', 'user', 'Profesor García', 'garcia@cadel.academy', 'Barcelona', 'Docente de Ciberseguridad con 10 años de experiencia.'),
            (3, 'alumno', '1234', 'user', 'Juan Pérez', 'juan@cadel.academy', 'Valencia', 'Estudiante entusiasta del hacking ético.'),
            (4, 'hacker', 'hacker123', 'user', 'Mr. Robot', 'elliot@fsociety.dat', 'Unknown', 'Hello friend.')
        ]
        
        for u in users:
            # Check if user exists to avoid auto-increment gaps or errors
            cursor.execute("SELECT id FROM users WHERE id = %s", (u[0],))
            if not cursor.fetchone():
                try:
                    cursor.execute(
                        "INSERT INTO users (id, username, password, role, full_name, email, city, bio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        u
                    )
                    conn.commit()
                except mysql.connector.Error:
                    pass # Ignore if inserted by other container
        
        # 2. Posts del Foro
        posts = [
            (1, 'Normas de la Academia', 'Bienvenidos al curso de Hacking Ético. Por favor, respetad las normas y no ataquéis infraestructura externa.', 1),
            (2, 'Duda sobre SQL Injection', 'Hola, estoy intentando hacer el ejercicio de login pero no me sale. ¿Alguna pista?', 3),
            (3, 'Recursos para XSS', 'Os comparto una lista de payloads interesantes para probar en el laboratorio.', 2),
            (4, '¿Alguien para estudiar?', 'Busco compañero para preparar la certificación CEH.', 3)
        ]

        for p in posts:
            # Verificamos si el post ya existe por ID
            cursor.execute("SELECT id FROM posts WHERE id = %s", (p[0],))
            if not cursor.fetchone():
                try:
                    cursor.execute("INSERT INTO posts (id, title, content, author_id) VALUES (%s, %s, %s, %s)", p)
                    conn.commit()
                except mysql.connector.Error:
                    pass

        # 3. Comentarios
        comments = [
            (2, 'Prueba con la comilla simple en el usuario.', 2),
            (2, 'Gracias profe! Ya lo conseguí.', 3),
            (3, 'Muy útil, gracias por compartir.', 4)
        ]

        for c in comments:
            # Verificamos si el comentario ya existe (por contenido y post_id)
            cursor.execute("SELECT id FROM comments WHERE content = %s AND post_id = %s", (c[1], c[0]))
            if not cursor.fetchone():
                try:
                    cursor.execute("INSERT INTO comments (post_id, content, author_id) VALUES (%s, %s, %s)", c)
                    conn.commit()
                except mysql.connector.Error:
                    pass

        # 4. Mensajes Privados de Chat
        private_messages = [
            (3, 2, 'Hola Profe, tengo una duda.'), # alumno -> profesor
            (2, 3, 'Hola Juan, dime en qué puedo ayudarte.'), # profesor -> alumno
            (4, 1, 'I am in.') # hacker -> admin
        ]
        
        for pm in private_messages:
            # Verificamos si el mensaje ya existe
            cursor.execute("SELECT id FROM private_messages WHERE message = %s AND sender_id = %s", (pm[2], pm[0]))
            if not cursor.fetchone():
                try:
                    cursor.execute("INSERT INTO private_messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)", pm)
                    conn.commit()
                except mysql.connector.Error:
                    pass
        
        print("Base de datos inicializada/verificada.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error durante init_db (puede ser concurrencia, ignorando): {e}")