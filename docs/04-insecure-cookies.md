# Auditoría: Gestión Insegura de Cookies

## Descripción
Las cookies de sesión son el mecanismo principal para mantener la autenticación del usuario. Si no se configuran con los atributos de seguridad adecuados, son vulnerables a robo y secuestro de sesión (Session Hijacking).

*   **Falta de `HttpOnly`:** Permite que JavaScript (y por tanto ataques XSS) acceda al contenido de la cookie.
*   **Falta de `Secure`:** Permite que la cookie se envíe a través de conexiones HTTP no cifradas, susceptible a intercepción (Man-in-the-Middle).

## 🕵️ Verificación y Reproducción

1.  Loguéate en la aplicación (`/login`).
2.  Abre las Herramientas de Desarrollador de tu navegador (F12).
3.  Ve a la pestaña **Aplicación** (Chrome) o **Almacenamiento** (Firefox) -> **Cookies**.
4.  Selecciona el dominio `localhost`.

**En Versión Vulnerable (Puerto 8080):**
*   Observa las columnas `HttpOnly` y `Secure`. Estarán vacías o desmarcadas.
*   Prueba en la consola: `document.cookie`. Verás el valor de `session` y `user_id`.

**En Versión Segura (Puerto 8443):**
*   Las columnas `HttpOnly` y `Secure` estarán marcadas con un check (✓).
*   Prueba en la consola: `document.cookie`. Devolverá una cadena vacía (protección contra robo por XSS).

## 🔍 Análisis del Código

**Código Vulnerable (`app/routes/login.py`):**

```python
if SECURITY_LEVEL == 'vulnerable':
    # Inseguro: Accesible por JS, viaja por HTTP plano, SameSite laxo
    resp.set_cookie('user_id', str(user['id']), httponly=False, secure=False, samesite='Lax')
else:
    # Seguro: Solo accesible por el servidor, solo viaja por HTTPS
    resp.set_cookie('user_id', str(user['id']), httponly=True, secure=True, samesite='Strict')
```

Además, la versión segura utiliza **Nginx** para forzar HTTPS y añadir cabeceras como HSTS (`Strict-Transport-Security`), evitando que las cookies viajen en texto plano.