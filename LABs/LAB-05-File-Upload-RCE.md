# Laboratorio 05: Unrestricted File Upload

## 🎯 Objetivo
Subir un archivo con contenido ejecutable (HTML/JS) aprovechando la falta de validación en el formulario de subida del foro.

## 📋 Prerrequisitos
1.  Sesión activa.
2.  Modo Vulnerable activo.

## 📝 Instrucciones Paso a Paso

### Paso 1: Preparar el Payload
1.  Crea un archivo en tu ordenador llamado `exploit.html`.
2.  Añade el siguiente contenido:
    ```html
    <html>
    <body>
        <h1>Archivo Malicioso</h1>
        <script>
            alert('XSS via File Upload: ' + document.domain);
        </script>
    </body>
    </html>
    ```

### Paso 2: Subida del Archivo
1.  Ve al **Foro**.
2.  En el formulario de "Crear Nueva Publicación", rellena un título cualquiera.
3.  En el campo de archivo, selecciona tu `exploit.html`.
4.  Publica el tema.

### Paso 3: Ejecución
1.  Busca tu publicación en el tablón.
2.  Verás un enlace al archivo adjunto.
3.  Haz clic en el enlace.

## 🏁 Verificación
*   El archivo HTML debe abrirse en el navegador y ejecutar el script (mostrar la alerta).
*   Esto demuestra que el servidor aceptó el archivo sin validar su extensión o contenido.

## 🛡️ Preguntas de Reflexión
1.  Si el servidor interpretara PHP, ¿qué podrías haber logrado subiendo un archivo `.php`?
2.  ¿Cómo se debería asegurar esta funcionalidad?
