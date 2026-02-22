# Laboratorio 01: SQL Injection (Bypass de Autenticación)

## 🎯 Objetivo
Lograr acceso administrativo a la plataforma sin conocer la contraseña del usuario 'admin', explotando una vulnerabilidad de Inyección SQL en el formulario de inicio de sesión.

## 📋 Prerrequisitos
1.  El entorno Docker debe estar corriendo (`docker-compose up`).
2.  Asegúrate de que el **Modo Vulnerable** (botón rojo) esté activo en la barra de navegación.
3.  Navegador web.

## 📝 Instrucciones Paso a Paso

### Paso 1: Reconocimiento
1.  Navega a la página de inicio de sesión: `http://localhost:8080/login`.
2.  Intenta iniciar sesión con credenciales aleatorias (ej. `test` / `test`) y observa el mensaje de error.

### Paso 2: Detección de Vulnerabilidad
1.  En el campo **Usuario**, introduce una comilla simple `'`.
2.  En el campo **Contraseña**, introduce cualquier cosa.
3.  Si la aplicación devuelve un error de base de datos o un comportamiento inesperado (como un error 500), es probable que sea vulnerable.

### Paso 3: Explotación (Bypass)
1.  Queremos inyectar una condición que siempre sea verdadera (`OR 1=1`) y comentar el resto de la consulta para anular la verificación de contraseña.
2.  Introduce el siguiente payload en el campo **Usuario**:
    ```sql
    admin' OR '1'='1' -- -
    ```
    *Nota: Asegúrate de incluir el espacio después del segundo guion.*
3.  Introduce cualquier valor en el campo **Contraseña**.
4.  Haz clic en "Entrar".

## 🏁 Verificación
*   Deberías ser redirigido al **Dashboard** o **Mi Perfil**.
*   Verifica que has iniciado sesión como el usuario **admin**.

## 🛡️ Preguntas de Reflexión
1.  ¿Por qué el uso de comillas simples rompe la consulta SQL original?
2.  ¿Qué hace exactamente la secuencia `-- -` o `#` al final de la inyección?
