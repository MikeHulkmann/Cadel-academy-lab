# Laboratorio 08: Open Redirect y Hijacking de Navegación

## 🎯 Objetivo
Identificar y explotar vulnerabilidades de redirección abierta para dirigir a los usuarios a sitios externos maliciosos, y diferenciar entre una redirección clásica y una basada en XSS.

## 📋 Prerrequisitos
1.  **Entorno:** Cadel Academy en Modo Vulnerable (`http://localhost:8080`).
2.  **Navegador Web** con herramientas de desarrollador (F12).

---

## 📝 Ejercicio 1: Explotación de Open Redirect Clásico

**Objetivo:** Abusar de una funcionalidad de redirección para enviar a un usuario a un sitio externo (YouTube).

### Paso 1: Descubrir el Endpoint de Redirección
1.  Durante la fase de reconocimiento, un auditor buscaría parámetros en la URL como `next`, `redirect`, `url`, `target`, etc.
2.  En Cadel Academy, hemos "descubierto" un endpoint en `http://localhost:8080/redirect`.

### Paso 2: Construir el Payload
1.  El endpoint espera un parámetro `target`. Vamos a construir una URL que apunte a YouTube.
2.  URL maliciosa:
    ```
    http://localhost:8080/redirect?target=https://www.youtube.com
    ```

### Paso 3: Ejecución y Verificación
1.  Abre las herramientas de desarrollador (F12) y ve a la pestaña **Red (Network)**.
2.  Pega la URL maliciosa en la barra de direcciones de tu navegador y pulsa Enter.
3.  **Observa la pestaña Red:** Verás una primera petición a `/redirect?target=...` que recibe una respuesta con código de estado **302 Found**.
4.  Selecciona esa petición y mira las cabeceras de respuesta. Verás una cabecera `Location: https://www.youtube.com`.
5.  **Resultado:** Tu navegador seguirá automáticamente esta cabecera y serás redirigido a YouTube.

---

## 📝 Ejercicio 2: Comparativa con Redirección vía XSS Stored

**Objetivo:** Recordar cómo se logra una redirección utilizando una vulnerabilidad de XSS Almacenado, como se vio en el **LAB-04b**.

### Paso 1: Inyectar el Payload XSS
1.  Ve al **Foro** y crea una nueva publicación.
2.  En el contenido, inyecta el siguiente script:
    ```html
    <script>window.location = "https://www.github.com";</script>
    ```
3.  Publica el tema.

### Paso 2: Verificación
1.  Cada vez que tú u otro usuario visite la página principal del foro, el script se ejecutará y el navegador será redirigido a GitHub.

---

## 🛡️ Preguntas de Reflexión

1.  **¿Cuál es la diferencia fundamental entre los dos ataques?**
    *   En el **Open Redirect**, el servidor es quien envía la orden de redirigir (cabecera `Location`). El navegador obedece.
    *   En la **Redirección por XSS**, el servidor entrega una página con código malicioso. Es el JavaScript, ejecutándose en el cliente, quien da la orden de redirigir.

2.  **¿Por qué un atacante preferiría un Open Redirect para un ataque de phishing?**
    *   Porque la URL inicial que la víctima ve pertenece a un dominio de confianza (ej. `https://banco.com/redirect?url=...`). Esto aumenta la probabilidad de que la víctima haga clic y confíe en la página de destino falsa.

3.  **¿Cómo se soluciona un Open Redirect en el modo seguro?**
    *   Revisa el código en `app/routes/help.py`. La solución implementada valida que la URL de destino sea relativa o pertenezca al mismo dominio, bloqueando cualquier intento de redirección externa.