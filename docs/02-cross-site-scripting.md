# Auditoría: Cross-Site Scripting (XSS)

## Descripción
El Cross-Site Scripting (XSS) es una vulnerabilidad de inyección de código que ocurre cuando una aplicación web incluye datos no confiables en una página web sin la validación o el escape adecuados. Esto permite que los scripts inyectados se ejecuten en el navegador de la víctima, permitiendo al atacante secuestrar sesiones de usuario, desfigurar sitios web o redirigir al usuario a sitios maliciosos.

## 🕵️ Vectores de Ataque Avanzados

### 1. XSS Almacenado (Stored / Persistent)
Esta es la variante más peligrosa. El script malicioso se guarda permanentemente en el servidor (base de datos, sistema de archivos, foros, campos de comentarios, etc.). La víctima recupera el script malicioso al visualizar el contenido almacenado.

#### Escenario A: Redirección Maliciosa (Open Redirect via XSS)
El atacante inyecta código JavaScript que fuerza al navegador de la víctima a navegar a una URL externa.
*   **Impacto:** Phishing, descarga de malware, daño reputacional.
*   **Mecánica:** Modificación del objeto `window.location`.

#### Escenario B: Exfiltración de Datos (Session Hijacking)
El atacante inyecta código que lee información sensible del navegador (como `document.cookie` o `localStorage`) y la envía a un servidor controlado por el atacante mediante una petición HTTP asíncrona (AJAX/Fetch).
*   **Impacto:** Compromiso total de la cuenta (Account Takeover).
*   **Mecánica:** Uso de `fetch()` o `Image()` para contactar al servidor C2 (Command & Control).

## 🛠️ Herramientas de Auditoría

*   **Burp Suite:** Proxy de interceptación esencial para modificar peticiones en vuelo, permitiendo inyectar payloads que podrían estar bloqueados por validaciones simples en el lado del cliente (HTML/JS).
*   **Python (`http.server`):** Utilidad para levantar rápidamente un servidor web ligero que actúe como receptor de los datos robados (Listener).
*   **Netcat (`nc`):** Herramienta de red versátil para escuchar conexiones entrantes.

## 🔍 Análisis del Código Vulnerable

**Ejemplo en `app/templates/search.html` o `forum.html`:**

```html
<!-- VULNERABLE: Uso del filtro 'safe' -->
{{ post.content | safe }}
```

El filtro `| safe` en Jinja2 indica explícitamente al motor de plantillas que **no escape** los caracteres HTML. Si `post.content` contiene `<script>...`, se ejecutará.

## 🛡️ Solución (Versión Segura)

La defensa principal contra XSS es el **Output Encoding** (Codificación de Salida). Se deben convertir los caracteres especiales en sus correspondientes entidades HTML antes de renderizarlos en el navegador.

**En Jinja2 (Python):**
Simplemente eliminar el filtro `| safe`. Jinja2 escapa automáticamente por defecto.

```html
<!-- SEGURO: Escape automático -->
{{ post.content }}
```

**Resultado del Escape:**
El payload `<script>alert(1)</script>` se convierte en:
`&lt;script&gt;alert(1)&lt;/script&gt;`

El navegador lo interpreta como texto seguro, no como código ejecutable.

### Medidas Adicionales (Defensa en Profundidad)

1.  **Content Security Policy (CSP):** Cabecera HTTP que restringe las fuentes desde las cuales el navegador puede cargar recursos (scripts, imágenes, etc.).
    *   Ejemplo: `Content-Security-Policy: default-src 'self';`
2.  **Cookies HttpOnly:** Configurar la bandera `HttpOnly` en las cookies de sesión impide que JavaScript (y por tanto, un ataque XSS) pueda leerlas mediante `document.cookie`.
    *   Implementado en `app/routes/login.py` (Modo Seguro).