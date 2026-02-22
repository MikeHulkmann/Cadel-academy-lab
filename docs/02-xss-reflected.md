# Auditoría: Cross-Site Scripting (Reflected)

## Descripción
El Cross-Site Scripting (XSS) Reflejado ocurre cuando una aplicación recibe datos en una petición HTTP (generalmente parámetros URL GET) e incluye esos datos en la respuesta inmediata sin escapar o validar correctamente. El script malicioso no se guarda en la base de datos, sino que "rebota" desde el servidor web.

## 🕵️ Reproducción

1.  Navega a `http://localhost:8080/search` (Modo Vulnerable).
2.  En la barra de búsqueda, introduce:
    ```html
    <script>alert('XSS Reflejado')</script>
    ```
3.  Pulsa "Buscar".

**Resultado:** Aparecerá una ventana de alerta en el navegador. El servidor ha devuelto el script tal cual en el HTML de respuesta y el navegador lo ha ejecutado.

**Impacto:** Un atacante podría enviar un enlace malicioso a una víctima (ej. por email) que, al hacer clic, ejecute acciones en su nombre o robe sus cookies de sesión.

## 🔍 Análisis del Código

**Template Vulnerable (`app/templates/search.html`):**
```html
<!-- El filtro 'safe' desactiva el escape automático de Jinja2 -->
{{ query | safe }}
```
El filtro `| safe` en Jinja2 le indica explícitamente al motor de plantillas que **NO** escape los caracteres HTML, confiando ciegamente en el input.

## 🛡️ Solución (Versión Segura)

Eliminar el filtro `safe` y permitir que el motor de plantillas realice el **Context-Aware Output Encoding** (comportamiento por defecto en Jinja2).

```html
{{ query }}
```
Esto convierte `<script>` en `&lt;script&gt;`, que se muestra como texto pero no se ejecuta.
