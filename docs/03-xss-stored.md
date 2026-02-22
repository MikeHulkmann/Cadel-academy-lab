# Auditoría: Cross-Site Scripting (Stored)

## Descripción
El XSS Almacenado (o Persistente) es una de las vulnerabilidades web más peligrosas. Ocurre cuando la aplicación guarda datos maliciosos proporcionados por el usuario en la base de datos (ej. comentarios, mensajes, perfiles) y luego los muestra a otros usuarios sin la debida sanitización. El script se ejecuta automáticamente en el navegador de cualquier víctima que visualice el contenido afectado.

## 🕵️ Vectores de Ataque y Reproducción

### Caso 1: Foro Público y Comentarios
1.  Navega a `http://localhost:8080/forum` o a un post individual.
2.  Crea una nueva publicación o comentario con el siguiente contenido:
    ```html
    <script>alert('XSS en Foro')</script>
    ```
3.  Cualquier usuario que visite el foro verá la alerta.

### Caso 2: Chat Privado
1.  Envía un mensaje a otro usuario (ej. al profesor) con un payload malicioso.
2.  Cuando el destinatario abra el chat, el código se ejecutará en su sesión.

### Caso 3: Perfil de Usuario
1.  Ve a "Mi Perfil" (`/profile`).
2.  En el campo "Bio" o "Nombre Completo", introduce:
    ```html
    <b>Hacker</b><script>console.log(document.cookie)</script>
    ```
3.  Guarda los cambios. El script se ejecutará cada vez que tú o un administrador vea tu perfil.

## 🔍 Análisis del Código

El problema radica en confiar en los datos recuperados de la base de datos y mostrarlos directamente en el HTML sin escapar.

**Template Vulnerable (`app/templates/forum.html`, `user.html`, etc.):**
```html
<!-- Se usa 'safe' para renderizar el contenido tal cual se guardó -->
{{ post.content | safe }}
{{ user.bio | safe }}
```

## 🛡️ Solución (Versión Segura)

Asegurar que todo contenido generado por el usuario se escape correctamente al renderizarse en el HTML.

```html
{{ comment.content }}
```
