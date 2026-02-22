from flask import Blueprint, render_template, abort

bp = Blueprint('blog', __name__)

# Base de datos estática de artículos del blog
ARTICLES = {
    "sql-injection-login": {
        "title": "Análisis Técnico: SQL Injection y Bypass de Autenticación",
        "date": "2026-02-20",
        "summary": "Estudio detallado sobre la manipulación de consultas SQL en mecanismos de autenticación y cómo la falta de sanitización permite el acceso no autorizado.",
        "content": """
            <p>La <strong>Inyección SQL (SQLi)</strong> es una vulnerabilidad de seguridad web que permite a un atacante interferir con las consultas que una aplicación realiza a su base de datos. En este artículo, analizaremos técnicamente cómo se produce un <em>Authentication Bypass</em>.</p>
            
            <h4>Fundamentos Teóricos</h4>
            <p>Las aplicaciones web interactúan con bases de datos mediante el lenguaje SQL (Structured Query Language). Una vulnerabilidad ocurre cuando los datos proporcionados por el usuario (input) se concatenan directamente con el código SQL sin la debida validación o escape, rompiendo la separación entre datos y comandos.</p>
            
            <h4>Análisis del Código Vulnerable</h4>
            <p>Consideremos el siguiente fragmento de código Python/Flask presente en el entorno vulnerable:</p>
            <pre><code class="language-python">query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"</code></pre>
            <p>Aquí, la variable <code>username</code> se inserta directamente dentro de las comillas simples de la consulta.</p>
            
            <h4>Vector de Ataque: Tautología</h4>
            <p>El objetivo es alterar la lógica booleana de la cláusula <code>WHERE</code>. Al introducir el payload <code>admin' OR '1'='1' -- -</code>, la consulta resultante interpretada por el motor de base de datos es:</p>
            <pre><code class="language-sql">SELECT * FROM users WHERE username = 'admin' OR '1'='1' -- -' AND password = '...'</code></pre>
            
            <ul>
                <li><code>'</code>: Cierra la cadena de texto del campo username.</li>
                <li><code>OR '1'='1'</code>: Introduce una condición que siempre se evalúa como <strong>VERDADERA</strong> (Tautología).</li>
                <li><code>--</code>: Es el indicador de comentario en SQL. Todo lo que sigue (la verificación de la contraseña) es ignorado por el motor.</li>
            </ul>
            
            <p>Como resultado, la base de datos devuelve el primer registro que cumple la condición (generalmente el administrador), permitiendo el acceso sin credenciales válidas.</p>

            <h4>Mitigación y Defensa en Profundidad</h4>
            <p>La defensa estándar de la industria es el uso de <strong>Consultas Parametrizadas (Prepared Statements)</strong>. En este modelo, la base de datos trata los parámetros como datos estrictos, nunca como código ejecutable, neutralizando la inyección independientemente del contenido del input.</p>
        """
    },
    "sql-injection-chat": {
        "title": "SQL Injection Avanzado: Exfiltración de Datos vía UNION",
        "date": "2026-02-21",
        "summary": "Metodología para la extracción de información sensible en bases de datos relacionales utilizando el operador UNION en puntos de inyección visibles.",
        "content": """
            <p>Cuando una inyección SQL ocurre en una sentencia <code>SELECT</code> y los resultados de dicha consulta se reflejan en la respuesta HTTP (In-band SQLi), es posible utilizar el operador <code>UNION</code> para combinar los resultados de la consulta original con los resultados de una consulta inyectada arbitraria.</p>
            
            <h4>Requisitos Técnicos para UNION SQLi</h4>
            <p>Para que un ataque UNION sea exitoso, deben cumplirse dos condiciones estrictas:</p>
            <ol>
                <li>La consulta inyectada debe devolver el <strong>mismo número de columnas</strong> que la consulta original.</li>
                <li>Los tipos de datos de las columnas correspondientes deben ser compatibles.</li>
            </ol>
            
            <h4>Metodología de Explotación</h4>
            <ol>
                <li><strong>Detección y Fuzzing:</strong> Identificar el punto de inyección (ej. buscador de usuarios) mediante caracteres especiales (<code>'</code>, <code>"</code>).</li>
                <li><strong>Enumeración de Columnas:</strong> Utilizar la cláusula <code>ORDER BY</code> para determinar el número de columnas proyectadas.
                    <br><code>' ORDER BY 1 -- -</code> (Éxito)
                    <br><code>' ORDER BY 5 -- -</code> (Fallo -> Error 500 o mensaje de error SQL).
                </li>
                <li><strong>Identificación de Columnas Visibles:</strong> Inyectar <code>UNION SELECT 1, 2, ... -- -</code> para ver qué números se reflejan en la interfaz.</li>
                <li><strong>Exfiltración:</strong> Reemplazar los números visibles por funciones de base de datos o consultas a tablas del sistema (<code>information_schema</code>).
                    <br>Payload: <code>' UNION SELECT 1, @@version -- -</code>
                </li>
            </ol>
            
            <h4>Automatización</h4>
            <p>Herramientas como <strong>SQLMap</strong> automatizan este proceso de inferencia y extracción, permitiendo volcar bases de datos completas (Database Dump) en minutos.</p>
        """
    },
    "xss-reflected": {
        "title": "Cross-Site Scripting (XSS) Reflejado: Mecánica e Impacto",
        "date": "2026-02-22",
        "summary": "Análisis del XSS no persistente, vectores de entrada a través de parámetros HTTP y su rol en ataques dirigidos de ingeniería social.",
        "content": """
            <p>El <strong>Cross-Site Scripting (XSS) Reflejado</strong> ocurre cuando una aplicación recibe datos en una petición HTTP (generalmente parámetros GET o POST) e incluye esos datos en la respuesta inmediata de forma insegura, sin la validación o el escape adecuados.</p>
            
            <h4>Mecánica del Ataque</h4>
            <p>A diferencia del XSS Almacenado, el script malicioso no reside en la base de datos del servidor. El flujo es el siguiente:</p>
            <ol>
                <li>El atacante construye una URL maliciosa que contiene el payload de JavaScript.</li>
                <li>La víctima es engañada (Ingeniería Social) para hacer clic en el enlace.</li>
                <li>El servidor recibe la petición y "refleja" el payload en el HTML de respuesta.</li>
                <li>El navegador de la víctima ejecuta el script creyendo que es código legítimo del sitio (Same Origin Policy).</li>
            </ol>
            
            <h4>Contexto de Ejecución</h4>
            <p>En Cadel Academy, el parámetro <code>q</code> del buscador se renderiza dentro de una etiqueta <code>&lt;p&gt;</code>. Al usar el filtro <code>| safe</code> en Jinja2, se deshabilita el <em>Context-Aware Output Encoding</em>, permitiendo la inyección de etiquetas <code>&lt;script&gt;</code>.</p>
            
            <h4>Impacto en la Seguridad</h4>
            <p>Aunque no es persistente, el XSS Reflejado permite:</p>
            <ul>
                <li><strong>Robo de Sesión:</strong> Acceso a <code>document.cookie</code>.</li>
                <li><strong>Phishing Avanzado:</strong> Modificación del DOM para presentar formularios de login falsos.</li>
                <li><strong>Acciones en nombre del usuario:</strong> Realizar peticiones HTTP (CSRF) usando la sesión de la víctima.</li>
            </ul>
        """
    },
    "xss-stored": {
        "title": "XSS Stored: Persistencia y Compromiso Masivo",
        "date": "2026-02-23",
        "summary": "Análisis de la variante persistente de XSS, su almacenamiento en bases de datos y su capacidad para comprometer usuarios sin interacción directa del atacante.",
        "content": """
            <p>El <strong>XSS Almacenado (Stored o Persistent)</strong> es considerado la variante más peligrosa de Cross-Site Scripting. Ocurre cuando la aplicación guarda el input malicioso en el servidor (base de datos, sistema de archivos, logs) y luego lo sirve a otros usuarios sin sanitización.</p>
            
            <h4>Vectores de Persistencia</h4>
            <p>En nuestra plataforma académica, existen múltiples puntos de inyección persistente:</p>
            <ul>
                <li><strong>Foros de Discusión:</strong> Un post malicioso afecta a cualquier lector del hilo.</li>
                <li><strong>Perfiles de Usuario:</strong> Inyecciones en campos como "Biografía" o "Nombre" se ejecutan al visualizar el perfil.</li>
                <li><strong>Mensajería:</strong> Permite ataques dirigidos (Spear Phishing) dentro de la plataforma.</li>
            </ul>
            
            <h4>Escenarios de Explotación Avanzada</h4>
            <ul>
                <li><strong>Gusanos XSS (Worms):</strong> Un script que no solo roba datos, sino que se replica a sí mismo publicando nuevos posts en nombre de la víctima, propagando la infección exponencialmente (ej. Gusano Samy de MySpace).</li>
                <li><strong>Hooking de Navegador:</strong> Integración con frameworks como <strong>BeEF</strong> para controlar el navegador de la víctima en tiempo real.</li>
                <li><strong>Keylogging:</strong> Inyección de event listeners para capturar pulsaciones de teclas y enviarlas a un servidor C2 (Command & Control).</li>
            </ul>
        """
    },
    "file-upload": {
        "title": "Vulnerabilidades en Subida de Archivos: De XSS a RCE",
        "date": "2026-02-24",
        "summary": "Estudio de los riesgos asociados a la gestión insegura de archivos adjuntos: ejecución remota de código, defacement y ataques al cliente.",
        "content": """
            <p>La funcionalidad de subida de archivos (File Upload) es un vector de ataque crítico si no se implementan controles estrictos sobre el tipo, contenido, nombre y tamaño de los archivos.</p>
            
            <h4>Riesgos de Seguridad</h4>
            <ol>
                <li><strong>Remote Code Execution (RCE):</strong> Si el servidor web está configurado para ejecutar scripts (como PHP, ASP, JSP) en el directorio de subidas, un atacante puede subir una <em>Web Shell</em> y tomar control total del sistema operativo.</li>
                <li><strong>XSS Stored (Client-Side):</strong> Subir archivos HTML, SVG o XML con scripts incrustados. Cuando otro usuario visualiza el archivo, el script se ejecuta en el contexto del dominio de la aplicación.</li>
                <li><strong>Denegación de Servicio (DoS):</strong> Subida de archivos masivos para agotar el espacio en disco o el ancho de banda.</li>
            </ol>
            
            <h4>Estrategias de Validación Segura</h4>
            <p>Para mitigar estos riesgos, se debe aplicar una defensa en profundidad:</p>
            <ul>
                <li><strong>Lista Blanca de Extensiones:</strong> Permitir explícitamente solo extensiones seguras (ej. <code>.jpg</code>, <code>.png</code>, <code>.pdf</code>).</li>
                <li><strong>Validación de Contenido (Magic Bytes):</strong> Verificar la cabecera del archivo para asegurar que coincide con la extensión.</li>
                <li><strong>Renombrado Aleatorio:</strong> Guardar el archivo con un UUID generado por el sistema para evitar colisiones y ejecución directa basada en nombres predecibles.</li>
                <li><strong>Almacenamiento Externo:</strong> Servir los archivos desde un dominio diferente o un bucket S3 para aislar el riesgo de XSS.</li>
            </ul>
        """
    },
    "insecure-cookies": {
        "title": "Seguridad en Cookies: HttpOnly, Secure y SameSite",
        "date": "2026-02-25",
        "summary": "Análisis técnico de los atributos de seguridad en cookies de sesión y su rol en la prevención de Session Hijacking y CSRF.",
        "content": """
            <p>Las cookies de sesión son el mecanismo estándar para mantener el estado en el protocolo HTTP (que es <em>stateless</em>). Su compromiso equivale al compromiso de la cuenta del usuario.</p>
            
            <h4>La Tríada de Seguridad de Cookies</h4>
            <ul>
                <li><strong>HttpOnly:</strong> Instruye al navegador para que la cookie no sea accesible a través de APIs del lado del cliente como <code>document.cookie</code>. Esto mitiga significativamente el impacto de vulnerabilidades XSS, ya que el atacante no puede leer el identificador de sesión.</li>
                <li><strong>Secure:</strong> Garantiza que la cookie solo se transmita a través de conexiones cifradas (HTTPS). Esto previene la interceptación de la sesión en ataques <em>Man-in-the-Middle</em> (MitM) en redes inseguras.</li>
                <li><strong>SameSite (Lax/Strict):</strong> Controla cuándo se envían las cookies en peticiones cross-site. Es la defensa principal contra ataques de Falsificación de Peticiones en Sitios Cruzados (CSRF).</li>
            </ul>
            
            <h4>Auditoría en Cadel Academy</h4>
            <p>En el <strong>Modo Vulnerable</strong>, estas banderas están desactivadas, permitiendo la demostración de robo de sesiones. En el <strong>Modo Seguro</strong>, se fuerzan todas las banderas y se utiliza Nginx para garantizar el transporte HTTPS.</p>
        """
    },
    "reconnaissance": {
        "title": "Reconocimiento Web: Enumeración y Divulgación de Información",
        "date": "2026-02-26",
        "summary": "Técnicas de OSINT y enumeración activa para descubrir activos ocultos, configuraciones expuestas y vectores de ataque no documentados.",
        "content": """
            <p>El reconocimiento es la fase preliminar y más importante de una auditoría de seguridad o prueba de penetración. Su objetivo es mapear la superficie de ataque de la aplicación.</p>
            
            <h4>Fuentes de Información Comunes</h4>
            <ul>
                <li><strong>robots.txt:</strong> Archivo diseñado para crawlers de buscadores, pero que a menudo revela rutas administrativas o sensibles que los desarrolladores quieren "ocultar".</li>
                <li><strong>Archivos de Respaldo y Configuración:</strong> Editores de texto y sistemas de control de versiones pueden dejar residuos como <code>.git/</code>, <code>.env</code>, <code>.bak</code> o <code>.old</code> accesibles públicamente.</li>
                <li><strong>Cabeceras HTTP:</strong> Revelan versiones de servidor (Banner Grabbing) y tecnologías utilizadas (ej. <code>X-Powered-By</code>).</li>
            </ul>
            
            <h4>Herramientas de Enumeración</h4>
            <p>El uso de herramientas automatizadas es estándar en esta fase:</p>
            <ul>
                <li><strong>Nmap:</strong> Escaneo de puertos y scripts NSE para descubrimiento de servicios web.</li>
                <li><strong>Gobuster / Dirb:</strong> Fuzzing de directorios y archivos basado en diccionarios para encontrar recursos no enlazados.</li>
                <li><strong>Wappalyzer:</strong> Identificación del stack tecnológico (Frameworks, CMS, Librerías JS).</li>
            </ul>
        """
    }
}

@bp.route('/blog')
def index():
    # Convertimos el diccionario a una lista para la plantilla, añadiendo el slug (clave)
    posts_list = []
    for slug, data in ARTICLES.items():
        post = data.copy()
        post['slug'] = slug
        posts_list.append(post)
    
    return render_template('blog.html', posts=posts_list)

@bp.route('/blog/<slug>')
def post(slug):
    article = ARTICLES.get(slug)
    if not article:
        abort(404)
    return render_template('blog_post.html', article=article)
